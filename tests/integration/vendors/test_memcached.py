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

    def test_celeryconfig(self, container: MemcachedContainer):
        expected_keys = {"url", "local_url", "hostname", "port"}
        assert set(container.celeryconfig.keys()) == expected_keys


@pytest.mark.parametrize("backend", [lazy_fixture(CELERY_MEMCACHED_BACKEND)])
class test_memcached_test_backend:
    @pytest.mark.skip("Placeholder")
    def test_placeholder(self, backend: MemcachedTestBackend):
        backend = backend
