from pytest_celery import MEMCACHED_ENV
from pytest_celery import MEMCACHED_IMAGE
from pytest_celery import MemcachedContainer
from pytest_celery import MemcachedTestBackend


class test_memcached_container:
    def test_client(self, memcached_test_container: MemcachedContainer):
        assert memcached_test_container.client

    def test_celeryconfig(self, memcached_test_container: MemcachedContainer):
        expected_keys = {"url", "local_url", "hostname", "port"}
        assert set(memcached_test_container.celeryconfig.keys()) == expected_keys

    def test_version(self, memcached_test_container: MemcachedContainer):
        assert memcached_test_container.version() == "latest"

    def test_env(self, memcached_test_container: MemcachedContainer):
        assert memcached_test_container.env() == MEMCACHED_ENV

    def test_image(self, memcached_test_container: MemcachedContainer):
        assert memcached_test_container.image() == MEMCACHED_IMAGE


class test_memcached_test_backend:
    def test_ready(self, celery_memcached_backend: MemcachedTestBackend):
        assert celery_memcached_backend.ready()
