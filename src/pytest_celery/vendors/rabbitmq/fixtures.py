# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery.vendors.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.vendors.rabbitmq.container import RabbitMQContainer
from pytest_celery.vendors.rabbitmq.defaults import RABBITMQ_CONTAINER_TIMEOUT


@pytest.fixture
def celery_rabbitmq_broker(default_rabbitmq_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    """Creates a RabbitMQTestBroker instance. Responsible for tearing down the
    node.

    Args:
        default_rabbitmq_broker (RabbitMQContainer): Instantiated RabbitMQContainer.
    """
    broker = RabbitMQTestBroker(default_rabbitmq_broker)
    yield broker
    broker.teardown()


@pytest.fixture
def default_rabbitmq_broker_cls() -> type[RabbitMQContainer]:
    return RabbitMQContainer


default_rabbitmq_broker = container(
    image="{default_rabbitmq_broker_image}",
    ports=fxtr("default_rabbitmq_broker_ports"),
    environment=fxtr("default_rabbitmq_broker_env"),
    network="{default_pytest_celery_network.name}",
    wrapper_class=RabbitMQContainer,
    timeout=RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_rabbitmq_broker_env(default_rabbitmq_broker_cls: type[RabbitMQContainer]) -> dict:
    yield default_rabbitmq_broker_cls.env()


@pytest.fixture
def default_rabbitmq_broker_image(default_rabbitmq_broker_cls: type[RabbitMQContainer]) -> str:
    yield default_rabbitmq_broker_cls.image()


@pytest.fixture
def default_rabbitmq_broker_ports(default_rabbitmq_broker_cls: type[RabbitMQContainer]) -> dict:
    yield default_rabbitmq_broker_cls.ports()
