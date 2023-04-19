# mypy: disable-error-code="misc"

from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer


@pytest.fixture
def celery_rabbitmq_broker(default_rabbitmq_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQTestBroker(default_rabbitmq_broker)
    broker.ready()
    yield broker
    broker.teardown()


@pytest.fixture
def default_rabbitmq_broker_cls() -> Type[RabbitMQContainer]:
    return RabbitMQContainer


default_rabbitmq_broker = container(
    image="{default_rabbitmq_broker_image}",
    ports=fxtr("default_rabbitmq_broker_ports"),
    environment=fxtr("default_rabbitmq_broker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_rabbitmq_broker_env(default_rabbitmq_broker_cls: Type[RabbitMQContainer]) -> dict:
    yield default_rabbitmq_broker_cls.env()


@pytest.fixture
def default_rabbitmq_broker_image(default_rabbitmq_broker_cls: Type[RabbitMQContainer]) -> str:
    yield default_rabbitmq_broker_cls.image()


@pytest.fixture
def default_rabbitmq_broker_ports(default_rabbitmq_broker_cls: Type[RabbitMQContainer]) -> dict:
    yield default_rabbitmq_broker_cls.ports()


@pytest.fixture
def default_rabbitmq_broker_celeryconfig(default_rabbitmq_broker: RabbitMQContainer) -> dict:
    yield {"broker_url": default_rabbitmq_broker.celeryconfig["url"]}
