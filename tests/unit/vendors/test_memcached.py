from pytest_celery import MEMCACHED_ENV
from pytest_celery import MEMCACHED_IMAGE
from pytest_celery import MemcachedContainer
from pytest_celery import MemcachedTestBackend


class test_memcached_container:
    def test_version(self):
        assert MemcachedContainer.version() == "latest"

    def test_env(self):
        assert MemcachedContainer.env() == MEMCACHED_ENV

    def test_image(self):
        assert MemcachedContainer.image() == MEMCACHED_IMAGE


class test_memcached_backend_api:
    def test_ready(self, celery_memcached_backend: MemcachedTestBackend):
        celery_memcached_backend.ready()
        celery_memcached_backend.container.ready.assert_called_once()
