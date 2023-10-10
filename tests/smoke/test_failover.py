# mypy: disable-error-code="misc"

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestSetup
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from pytest_celery import defaults
from tests.tasks import identity

failover_broker = container(
    image="{default_rabbitmq_broker_image}",
    ports=fxtr("default_rabbitmq_broker_ports"),
    environment=fxtr("default_rabbitmq_broker_env"),
    network="{default_pytest_celery_network.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def failover_rabbitmq_broker(failover_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(failover_broker)
    yield broker
    broker.teardown()


@pytest.fixture
def celery_broker_cluster(
    celery_rabbitmq_broker: RabbitMQTestBroker,
    failover_rabbitmq_broker: RabbitMQTestBroker,
) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(celery_rabbitmq_broker, failover_rabbitmq_broker)
    yield cluster
    cluster.teardown()


class test_failover:
    def test_broker_failover(self, celery_setup: CeleryTestSetup):
        assert 3 <= len(celery_setup) <= 6
        assert len(celery_setup.broker_cluster) == 2
        celery_setup.broker_cluster[0].kill()
        for worker in celery_setup.worker_cluster:
            expected = "test_broker_failover"
            res = identity.s(expected).apply_async(queue=worker.worker_queue)
            assert res.get(timeout=defaults.RESULT_TIMEOUT) == expected
