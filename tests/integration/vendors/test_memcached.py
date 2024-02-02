from __future__ import annotations

import pytest

from pytest_celery import CELERY_MEMCACHED_BACKEND
from pytest_celery import MemcachedContainer
from pytest_celery import MemcachedTestBackend
from tests.defaults import ALL_MEMCACHED_FIXTURES


@pytest.mark.parametrize("container", ALL_MEMCACHED_FIXTURES)
class test_memcached_container:
    def test_client(self, container: MemcachedContainer, request):
        container = request.getfixturevalue(container)
        assert container.client
        assert not container.client.touch("ready", 1)
        assert container.client.set("ready", "1")
        assert container.client.get("ready") == "1"
        assert container.client.delete("ready")

    def test_celeryconfig(self, container: MemcachedContainer, request):
        container = request.getfixturevalue(container)
        expected_keys = {"url", "host_url", "hostname", "port"}
        config = container.celeryconfig
        assert set(config.keys()) == expected_keys
        assert container.prefix() in config["url"]
        assert container.prefix() in config["host_url"]


@pytest.mark.parametrize("backend", [CELERY_MEMCACHED_BACKEND])
class test_memcached_test_backend:
    def test_config(self, backend: MemcachedTestBackend, request):
        backend = request.getfixturevalue(backend)
        expected_keys = {"url", "host_url", "hostname", "port"}
        assert set(backend.config().keys()) == expected_keys
        assert backend.container.prefix() in backend.config()["url"]
        assert backend.container.prefix() in backend.config()["host_url"]
