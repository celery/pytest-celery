from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.broker.redis.api import RedisTestBroker
from pytest_celery.containers.redis import RedisContainer


@pytest.fixture
def celery_redis_broker(default_redis_broker: RedisContainer) -> RedisTestBroker:
    return RedisTestBroker(default_redis_broker)


@pytest.fixture
def default_redis_broker_cls() -> Type[RedisContainer]:
    return RedisContainer


default_redis_broker = container(
    image="{default_redis_broker_image}",
    ports=fxtr("default_redis_broker_ports"),
    environment=fxtr("default_redis_broker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_redis_broker_env(default_redis_broker_cls: Type[RedisContainer]) -> dict:
    return default_redis_broker_cls.env()


@pytest.fixture
def default_redis_broker_image(default_redis_broker_cls: Type[RedisContainer]) -> str:
    return default_redis_broker_cls.image()


@pytest.fixture
def default_redis_broker_ports(default_redis_broker_cls: Type[RedisContainer]) -> dict:
    return default_redis_broker_cls.ports()


@pytest.fixture
def default_redis_broker_celeryconfig(default_redis_broker: RedisContainer) -> dict:
    return {"broker_url": default_redis_broker.celeryconfig["url"]}
