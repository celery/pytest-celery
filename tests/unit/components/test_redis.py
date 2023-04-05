from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker


class test_redis_test_backend:
    def test_ready(self, celery_redis_backend: RedisTestBackend):
        assert celery_redis_backend.ready()


class test_redis_test_broker:
    def test_ready(self, celery_redis_broker: RedisTestBroker):
        assert celery_redis_broker.ready()
