"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Memcached Backend vendor.
"""

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
    """Default Memcached backend container class. Override to apply custom
    configuration globally.

    See also: :ref:`vendor-class`.

    Returns:
        type[MemcachedContainer]: API for managing the vendor's container.
    """
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
    """Environment variables for this vendor.

    Args:
        default_memcached_backend_cls (type[MemcachedContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Items to pass to the container's environment.
    """
    return default_memcached_backend_cls.initial_env()


@pytest.fixture
def default_memcached_backend_image(default_memcached_backend_cls: type[MemcachedContainer]) -> str:
    """Docker image for this vendor.

    Args:
        default_memcached_backend_cls (type[MemcachedContainer]): See also: :ref:`vendor-class`.

    Returns:
        str: Docker image name.
    """
    return default_memcached_backend_cls.image()


@pytest.fixture
def default_memcached_backend_ports(default_memcached_backend_cls: type[MemcachedContainer]) -> dict:
    """Port bindings for this vendor.

    Args:
        default_memcached_backend_cls (type[MemcachedContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Port bindings.
    """
    return default_memcached_backend_cls.ports()
