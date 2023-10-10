# mypy: disable-error-code="misc"

from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.vendors.redis.backend.api import RedisTestBackend
from pytest_celery.vendors.redis.container import RedisContainer


@pytest.fixture
def celery_redis_backend(default_redis_backend: RedisContainer) -> RedisTestBackend:
    backend = RedisTestBackend(default_redis_backend)
    yield backend
    backend.teardown()


@pytest.fixture
def default_redis_backend_cls() -> Type[RedisContainer]:
    return RedisContainer


default_redis_backend = container(
    image="{default_redis_backend_image}",
    ports=fxtr("default_redis_backend_ports"),
    environment=fxtr("default_redis_backend_env"),
    network="{default_pytest_celery_network.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_redis_backend_env(default_redis_backend_cls: Type[RedisContainer]) -> dict:
    yield default_redis_backend_cls.env()


@pytest.fixture
def default_redis_backend_image(default_redis_backend_cls: Type[RedisContainer]) -> str:
    yield default_redis_backend_cls.image()


@pytest.fixture
def default_redis_backend_ports(default_redis_backend_cls: Type[RedisContainer]) -> dict:
    yield default_redis_backend_cls.ports()