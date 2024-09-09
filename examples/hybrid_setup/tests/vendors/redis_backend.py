import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fetch

from pytest_celery import REDIS_CONTAINER_TIMEOUT
from pytest_celery import REDIS_ENV
from pytest_celery import REDIS_IMAGE
from pytest_celery import REDIS_PORTS
from pytest_celery import RedisContainer
from pytest_celery import RedisTestBackend

redis_image = fetch(repository=REDIS_IMAGE)
redis_test_container = container(
    # name="Redis-Session-Backend",  # Optional | Incompatible with parallel execution
    image="{redis_image.id}",
    scope="session",
    ports=REDIS_PORTS,
    environment=REDIS_ENV,
    network="{hybrid_setup_example_network.name}",
    wrapper_class=RedisContainer,
    timeout=REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def session_redis_backend(redis_test_container: RedisContainer) -> RedisTestBackend:
    backend = RedisTestBackend(redis_test_container)
    yield backend
    backend.teardown()
