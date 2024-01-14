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
    return RedisContainer


default_redis_broker = container(
    image="{default_redis_broker_image}",
    ports=fxtr("default_redis_broker_ports"),
    environment=fxtr("default_redis_broker_env"),
    network="{default_pytest_celery_network.name}",
    wrapper_class=RedisContainer,
    timeout=REDIS_CONTAINER_TIMEOUT,
    command=RedisContainer.command("--maxclients", "100000"),
)


@pytest.fixture
def default_redis_broker_env(default_redis_broker_cls: type[RedisContainer]) -> dict:
    return default_redis_broker_cls.env()


@pytest.fixture
def default_redis_broker_image(default_redis_broker_cls: type[RedisContainer]) -> str:
    return default_redis_broker_cls.image()


@pytest.fixture
def default_redis_broker_ports(default_redis_broker_cls: type[RedisContainer]) -> dict:
    return default_redis_broker_cls.ports()
