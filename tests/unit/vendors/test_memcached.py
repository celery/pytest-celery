import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_MEMCACHED_BACKEND
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


@pytest.mark.parametrize("backend", [lazy_fixture(CELERY_MEMCACHED_BACKEND)])
class test_memcached_backend_api:
    def test_ready(self, backend: MemcachedTestBackend):
        backend.ready()
        backend.container.ready.assert_called_once()
