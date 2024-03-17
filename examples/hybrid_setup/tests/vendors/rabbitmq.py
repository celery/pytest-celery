import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fetch

from pytest_celery import RABBITMQ_CONTAINER_TIMEOUT
from pytest_celery import RABBITMQ_ENV
from pytest_celery import RABBITMQ_IMAGE
from pytest_celery import RABBITMQ_PORTS
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker

rabbitmq_image = fetch(repository=RABBITMQ_IMAGE)

rabbitmq_test_container = container(
    # name="Main RabbitMQ Broker (session)",  # Optional | Incompatible with parallel execution
    image="{rabbitmq_image.id}",
    scope="session",
    ports=RABBITMQ_PORTS,
    environment=RABBITMQ_ENV,
    network="{hybrid_setup_example_network.name}",
    wrapper_class=RabbitMQContainer,
    timeout=RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def session_rabbitmq_broker(rabbitmq_test_container: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(rabbitmq_test_container)
    yield broker
    broker.teardown()


failover_test_container = container(
    # name="Failover RabbitMQ Broker (session)",  # Optional | Incompatible with parallel execution
    image="{rabbitmq_image.id}",
    scope="session",
    ports=RABBITMQ_PORTS,
    environment=RABBITMQ_ENV,
    network="{hybrid_setup_example_network.name}",
    wrapper_class=RabbitMQContainer,
    timeout=RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def session_failover_broker(failover_test_container: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(failover_test_container)
    yield broker
    broker.teardown()
