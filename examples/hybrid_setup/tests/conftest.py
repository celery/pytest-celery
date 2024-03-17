# flake8: noqa

import pytest
from pytest_docker_tools import network

from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from pytest_celery import MemcachedTestBackend
from tests.vendors.memcached import *
from tests.vendors.rabbitmq import *
from tests.vendors.workers.gevent import *
from tests.vendors.workers.legacy import *

# ----------------------------

hybrid_setup_example_network = network(scope="session")


@pytest.fixture
def celery_broker_cluster(
    session_rabbitmq_broker: RabbitMQTestBroker,
    session_failover_broker: RabbitMQTestBroker,
) -> CeleryBrokerCluster:
    """This is like setting broker_url to
    "session_rabbitmq_broker;session_failover_broker"."""
    cluster = CeleryBrokerCluster(
        session_rabbitmq_broker,
        session_failover_broker,
    )
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_backend_cluster(session_memcached_backend: MemcachedTestBackend) -> CeleryBackendCluster:
    cluster = CeleryBackendCluster(session_memcached_backend)
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_worker_cluster(
    gevent_worker: CeleryTestWorker,
    legacy_worker: CeleryTestWorker,
) -> CeleryWorkerCluster:
    cluster = CeleryWorkerCluster(gevent_worker, legacy_worker)
    yield cluster
    cluster.teardown()


@pytest.fixture
def default_worker_tasks(default_worker_tasks: set) -> set:
    from tests.vendors.workers import tasks

    default_worker_tasks.add(tasks)
    return default_worker_tasks


@pytest.fixture
def default_worker_signals(default_worker_signals: set) -> set:
    from tests.vendors.workers import signals

    default_worker_signals.add(signals)
    return default_worker_signals
