"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Redis Broker vendor.
"""

# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery.vendors.redis.broker.api import RedisTestBroker
from pytest_celery.vendors.redis.container import RedisContainer
from pytest_celery.vendors.redis.defaults import REDIS_CONTAINER_TIMEOUT


@pytest.fixture
def celery_redis_broker(default_redis_broker: RedisContainer) -> RedisTestBroker:
    """Creates a RedisTestBroker instance. Responsible for tearing down the
    node.

    Args:
        default_redis_broker (RedisContainer): Instantiated RedisContainer.
    """
    broker = RedisTestBroker(default_redis_broker)
    yield broker
    broker.teardown()


@pytest.fixture
def default_redis_broker_cls() -> type[RedisContainer]:
    """Default Redis broker container class. Override to apply custom
    configuration globally.

    See also: :ref:`vendor-class`.

    Returns:
        type[RedisContainer]: API for managing the vendor's container.
    """
    return RedisContainer


default_redis_broker = container(
    image="{default_redis_broker_image}",
    ports=fxtr("default_redis_broker_ports"),
    environment=fxtr("default_redis_broker_env"),
    network="{default_pytest_celery_network.name}",
    wrapper_class=RedisContainer,
    timeout=REDIS_CONTAINER_TIMEOUT,
    command=fxtr("default_redis_broker_command"),
)


@pytest.fixture
def default_redis_broker_command(default_redis_broker_cls: type[RedisContainer]) -> list[str]:
    """Command to run the container.

    Args:
        default_redis_broker_cls (type[RedisContainer]): See also: :ref:`vendor-class`.

    Returns:
        list[str]: Docker CMD instruction.
    """
    return default_redis_broker_cls.command()


@pytest.fixture
def default_redis_broker_env(default_redis_broker_cls: type[RedisContainer]) -> dict:
    """Environment variables for this vendor.

    Args:
        default_rabbitmq_broker_cls (type[RedisContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Items to pass to the container's environment.
    """
    return default_redis_broker_cls.initial_env()


@pytest.fixture
def default_redis_broker_image(default_redis_broker_cls: type[RedisContainer]) -> str:
    """Sets the image name for this vendor.

    Args:
        default_rabbitmq_broker_cls (type[RedisContainer]): See also: :ref:`vendor-class`.

    Returns:
        str: Docker image name.
    """
    return default_redis_broker_cls.image()


@pytest.fixture
def default_redis_broker_ports(default_redis_broker_cls: type[RedisContainer]) -> dict:
    """Port bindings for this vendor.

    Args:
        default_redis_broker_cls (type[RedisContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Port bindings.
    """
    return default_redis_broker_cls.ports()
