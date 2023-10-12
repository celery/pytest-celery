import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_MEMCACHED_BACKEND
from pytest_celery import MemcachedContainer
from pytest_celery import MemcachedTestBackend
from tests.defaults import ALL_MEMCACHED_FIXTURES


@pytest.mark.parametrize("container", lazy_fixture(ALL_MEMCACHED_FIXTURES))
class test_memcached_container:
    def test_client(self, container: MemcachedContainer):
        assert container.client
        assert not container.client.touch("ready", 1)
        assert container.client.set("ready", "1")
        assert container.client.get("ready") == "1"
        assert container.client.delete("ready")


@pytest.mark.parametrize("node", [lazy_fixture(CELERY_MEMCACHED_BACKEND)])
class test_memcached_test_backend:
    def test_ready(self, node: MemcachedTestBackend):
        assert node.ready()
