import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_REDIS_BACKEND
from pytest_celery import CELERY_REDIS_BROKER
from pytest_celery import REDIS_ENV
from pytest_celery import REDIS_IMAGE
from pytest_celery import RedisContainer
from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker


class test_redis_container:
    def test_version(self):
        assert RedisContainer.version() == "latest"

    def test_env(self):
        assert RedisContainer.env() == REDIS_ENV

    def test_image(self):
        assert RedisContainer.image() == REDIS_IMAGE


@pytest.mark.parametrize("backend", [lazy_fixture(CELERY_REDIS_BACKEND)])
class test_redis_backend_api:
    def test_ready(self, backend: RedisTestBackend):
        backend.ready()
        backend.container.ready.assert_called_once()


@pytest.mark.parametrize("broker", [lazy_fixture(CELERY_REDIS_BROKER)])
class test_redis_broker_api:
    def test_ready(self, broker: RedisTestBroker):
        broker.ready()
        broker.container.ready.assert_called_once()
