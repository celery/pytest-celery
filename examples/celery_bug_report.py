from __future__ import annotations

import pytest
from celery import Celery
from celery.canvas import Signature
from celery.result import AsyncResult

from pytest_celery import RABBITMQ_PORTS
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestSetup
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from pytest_celery import RedisTestBackend
from pytest_celery import ping

###############################################################################
# RabbitMQ Management Broker
###############################################################################


class RabbitMQManagementTestBroker(RabbitMQTestBroker):
    def get_management_url(self) -> str:
        """Opening this link during debugging allows you to see the RabbitMQ
        management UI in your browser."""
        ports = self.container.attrs["NetworkSettings"]["Ports"]
        ip = ports["15672/tcp"][0]["HostIp"]
        port = ports["15672/tcp"][0]["HostPort"]
        return f"http://{ip}:{port}"


@pytest.fixture
def default_rabbitmq_broker_image() -> str:
    return "rabbitmq:management"


@pytest.fixture
def default_rabbitmq_broker_ports() -> dict:
    # Expose the management UI port
    ports = RABBITMQ_PORTS.copy()
    ports.update({"15672/tcp": None})
    return ports


@pytest.fixture
def celery_rabbitmq_broker(default_rabbitmq_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQManagementTestBroker(default_rabbitmq_broker)
    yield broker
    broker.teardown()


@pytest.fixture
def celery_broker_cluster(celery_rabbitmq_broker: RabbitMQTestBroker) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(celery_rabbitmq_broker)
    yield cluster
    cluster.teardown()


###############################################################################
# Redis Result Backend
###############################################################################


@pytest.fixture
def celery_backend_cluster(celery_redis_backend: RedisTestBackend) -> CeleryBackendCluster:
    cluster = CeleryBackendCluster(celery_redis_backend)
    yield cluster
    cluster.teardown()


@pytest.fixture
def default_redis_backend_image() -> str:
    return "redis:latest"


###############################################################################
# Worker Configuration
###############################################################################


@pytest.fixture(scope="session")
def default_worker_celery_version() -> str:
    return "5.2.7"


@pytest.fixture(scope="session")
def default_worker_celery_log_level() -> str:
    return "INFO"


@pytest.fixture(scope="session")
def default_worker_celery_worker_queue() -> str:
    return "celery"


@pytest.fixture
def default_worker_command(default_worker_command: list[str]) -> list[str]:
    return default_worker_command + [
        "--without-gossip",
        "--without-mingle",
        "--without-heartbeat",
    ]


@pytest.fixture
def default_worker_app(default_worker_app: Celery) -> Celery:
    app = default_worker_app
    # app.conf...  # Add any additional configuration here
    return app


###############################################################################
# Bug Reproduction
###############################################################################


def test_issue_1234(celery_setup: CeleryTestSetup):
    sig: Signature = ping.s()
    res: AsyncResult = sig.delay()
    assert res.get() == "pong"
