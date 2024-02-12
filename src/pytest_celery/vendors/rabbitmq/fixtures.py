"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the RabbitMQ Broker vendor.
"""

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
    """Default RabbitMQ broker container class. Override to apply custom
    configuration globally.

    See also: :ref:`vendor-class`.

    Returns:
        type[RabbitMQContainer]: API for managing the vendor's container.
    """
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
    """Environment variables for this vendor.

    Args:
        default_rabbitmq_broker_cls (type[RabbitMQContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Items to pass to the container's environment.
    """
    return default_rabbitmq_broker_cls.initial_env()


@pytest.fixture
def default_rabbitmq_broker_image(default_rabbitmq_broker_cls: type[RabbitMQContainer]) -> str:
    """Sets the image name for this vendor.

    Args:
        default_rabbitmq_broker_cls (type[RabbitMQContainer]): See also: :ref:`vendor-class`.

    Returns:
        str: Docker image name.
    """
    return default_rabbitmq_broker_cls.image()


@pytest.fixture
def default_rabbitmq_broker_ports(default_rabbitmq_broker_cls: type[RabbitMQContainer]) -> dict:
    """Port bindings for this vendor.

    Args:
        default_rabbitmq_broker_cls (type[RabbitMQContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Port bindings.
    """
    return default_rabbitmq_broker_cls.ports()
