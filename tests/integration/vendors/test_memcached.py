from __future__ import annotations

import pytest

from pytest_celery import MemcachedContainer
from pytest_celery import MemcachedTestBackend
from tests.defaults import ALL_MEMCACHED_FIXTURES


@pytest.fixture
def container(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("container", ALL_MEMCACHED_FIXTURES, indirect=["container"])
class test_memcached_container:
    def test_client(self, container: MemcachedContainer):
        assert container.client
        assert not container.client.touch("ready", 1)
        assert container.client.set("ready", "1")
        assert container.client.get("ready") == "1"
        assert container.client.delete("ready")

    def test_celeryconfig(self, container: MemcachedContainer):
        expected_keys = {"url", "host_url", "hostname", "port"}
        config = container.celeryconfig
        assert set(config.keys()) == expected_keys
        assert container.prefix() in config["url"]
        assert container.prefix() in config["host_url"]


class test_memcached_test_backend:
    def test_config(self, celery_memcached_backend: MemcachedTestBackend):
        expected_keys = {"url", "host_url", "hostname", "port"}
        assert set(celery_memcached_backend.config().keys()) == expected_keys
        assert celery_memcached_backend.container.prefix() in celery_memcached_backend.config()["url"]
        assert celery_memcached_backend.container.prefix() in celery_memcached_backend.config()["host_url"]
