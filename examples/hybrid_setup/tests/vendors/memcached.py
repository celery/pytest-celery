import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fetch

from pytest_celery import MEMCACHED_CONTAINER_TIMEOUT
from pytest_celery import MEMCACHED_ENV
from pytest_celery import MEMCACHED_IMAGE
from pytest_celery import MEMCACHED_PORTS
from pytest_celery import MemcachedContainer
from pytest_celery import MemcachedTestBackend

memcached_image = fetch(repository=MEMCACHED_IMAGE)
memcached_test_container = container(
    # name="Memcached-Session-Backend",  # Optional | Incompatible with parallel execution
    image="{memcached_image.id}",
    scope="session",
    ports=MEMCACHED_PORTS,
    environment=MEMCACHED_ENV,
    network="{hybrid_setup_example_network.name}",
    wrapper_class=MemcachedContainer,
    timeout=MEMCACHED_CONTAINER_TIMEOUT,
)


@pytest.fixture
def session_memcached_backend(memcached_test_container: MemcachedContainer) -> MemcachedTestBackend:
    backend = MemcachedTestBackend(memcached_test_container)
    yield backend
    backend.teardown()
