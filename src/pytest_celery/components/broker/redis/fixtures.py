from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.broker.redis.api import RedisTestBroker
from pytest_celery.containers.redis import RedisContainer


@pytest.fixture
def celery_redis_broker(redis_function_broker: RedisContainer) -> RedisTestBroker:
    return RedisTestBroker(redis_function_broker)


@pytest.fixture
def redis_function_broker_cls() -> Type[RedisContainer]:
    return RedisContainer


redis_function_broker = container(
    image="{redis_function_broker_image}",
    ports=fxtr("redis_function_broker_ports"),
    environment=fxtr("redis_function_broker_env"),
    network="{DEFAULT_NETWORK.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def redis_function_broker_env(redis_function_broker_cls: Type[RedisContainer]) -> dict:
    return redis_function_broker_cls.env()


@pytest.fixture
def redis_function_broker_image(redis_function_broker_cls: Type[RedisContainer]) -> str:
    return redis_function_broker_cls.image()


@pytest.fixture
def redis_function_broker_ports(redis_function_broker_cls: Type[RedisContainer]) -> dict:
    return redis_function_broker_cls.ports()


@pytest.fixture
def redis_function_broker_celeryconfig(redis_function_broker: RedisContainer) -> dict:
    return {"broker_url": redis_function_broker.celeryconfig()["url"]}
