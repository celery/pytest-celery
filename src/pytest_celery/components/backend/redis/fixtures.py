import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.components.backend.redis.api import RedisTestBackend
from pytest_celery.components.container.redis import RedisContainer


@pytest.fixture(params=[defaults.CELERY_REDIS_BACKEND])
def celery_redis_backend(request: pytest.FixtureRequest) -> RedisTestBackend:
    return RedisTestBackend(request.getfixturevalue(request.param))


redis_function_backend = container(
    image="{redis_function_backend_image}",
    ports=fxtr("redis_function_backend_ports"),
    environment=fxtr("redis_function_backend_env"),
    wrapper_class=RedisContainer,
)


@pytest.fixture
def redis_function_backend_env() -> dict:
    return defaults.REDIS_FUNCTION_BACKEND_ENV


@pytest.fixture
def redis_function_backend_image() -> str:
    return defaults.REDIS_FUNCTION_BACKEND_IMAGE


@pytest.fixture
def redis_function_backend_ports() -> dict:
    return defaults.REDIS_FUNCTION_BACKEND_PORTS


redis_session_backend = container(
    image="{redis_session_backend_image}",
    scope="session",
    ports=fxtr("redis_session_backend_ports"),
    environment=fxtr("redis_session_backend_env"),
    wrapper_class=RedisContainer,
)


@pytest.fixture(scope="session")
def redis_session_backend_env() -> dict:
    return defaults.REDIS_SESSION_BACKEND_ENV


@pytest.fixture(scope="session")
def redis_session_backend_image() -> str:
    return defaults.REDIS_SESSION_BACKEND_IMAGE


@pytest.fixture(scope="session")
def redis_session_backend_ports() -> dict:
    return defaults.REDIS_SESSION_BACKEND_PORTS
