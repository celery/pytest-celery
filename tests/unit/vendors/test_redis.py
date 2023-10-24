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


class test_redis_backend_api:
    def test_ready(self, celery_redis_backend: RedisTestBackend):
        celery_redis_backend.ready()
        celery_redis_backend.container.ready.assert_called_once()


class test_redis_broker_api:
    def test_ready(self, celery_redis_broker: RedisTestBroker):
        celery_redis_broker.ready()
        celery_redis_broker.container.ready.assert_called_once()
