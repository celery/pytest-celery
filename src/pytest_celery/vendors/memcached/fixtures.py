# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery.vendors.memcached.api import MemcachedTestBackend
from pytest_celery.vendors.memcached.container import MemcachedContainer
from pytest_celery.vendors.memcached.defaults import MEMCACHED_CONTAINER_TIMEOUT


@pytest.fixture
def celery_memcached_backend(default_memcached_backend: MemcachedContainer) -> MemcachedTestBackend:
    """Creates a MemcachedTestBackend instance. Responsible for tearing down
    the node.

    Args:
        default_memcached_backend (MemcachedContainer): Instantiated MemcachedContainer.
    """
    backend = MemcachedTestBackend(default_memcached_backend)
    yield backend
    backend.teardown()


@pytest.fixture
def default_memcached_backend_cls() -> type[MemcachedContainer]:
    return MemcachedContainer


default_memcached_backend = container(
    image="{default_memcached_backend_image}",
    ports=fxtr("default_memcached_backend_ports"),
    environment=fxtr("default_memcached_backend_env"),
    network="{default_pytest_celery_network.name}",
    wrapper_class=MemcachedContainer,
    timeout=MEMCACHED_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_memcached_backend_env(default_memcached_backend_cls: type[MemcachedContainer]) -> dict:
    return default_memcached_backend_cls.env()


@pytest.fixture
def default_memcached_backend_image(default_memcached_backend_cls: type[MemcachedContainer]) -> str:
    return default_memcached_backend_cls.image()


@pytest.fixture
def default_memcached_backend_ports(default_memcached_backend_cls: type[MemcachedContainer]) -> dict:
    return default_memcached_backend_cls.ports()
