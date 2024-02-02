from __future__ import annotations

import pytest

from pytest_celery import CELERY_MEMCACHED_BACKEND
from pytest_celery import MEMCACHED_ENV
from pytest_celery import MEMCACHED_IMAGE
from pytest_celery import MEMCACHED_PORTS
from pytest_celery import MEMCACHED_PREFIX
from pytest_celery import MemcachedContainer
from pytest_celery import MemcachedTestBackend


class test_memcached_container:
    def test_version(self):
        assert MemcachedContainer.version() == "latest"

    def test_env(self):
        assert MemcachedContainer.env() == MEMCACHED_ENV

    def test_image(self):
        assert MemcachedContainer.image() == MEMCACHED_IMAGE

    def test_ports(self):
        assert MemcachedContainer.ports() == MEMCACHED_PORTS

    def test_prefix(self):
        assert MemcachedContainer.prefix() == MEMCACHED_PREFIX


@pytest.mark.parametrize("backend", [CELERY_MEMCACHED_BACKEND])
class test_memcached_backend_api:
    @pytest.mark.skip(reason="Placeholder")
    def test_placeholder(self, backend: MemcachedTestBackend, request):
        # The class MemcachedTestBackend is currently a placeholder
        # so we don't have any specific tests for it yet.
        # This test suite is pre-configured to test the MemcachedTestBackend
        # and ready to be used once the class is implemented.
        pass
