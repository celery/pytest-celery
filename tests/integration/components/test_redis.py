import pytest

from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker
from pytest_celery import defaults
from pytest_celery.utils import resilient_lazy_fixture as lazy_fixture


@pytest.mark.parametrize("node", [lazy_fixture(defaults.CELERY_REDIS_BACKEND)])
class test_redis_test_backend:
    def test_ready(self, node: RedisTestBackend):
        assert node.ready()


@pytest.mark.parametrize("node", [lazy_fixture(defaults.CELERY_REDIS_BROKER)])
class test_redis_test_broker:
    def test_ready(self, node: RedisTestBroker):
        assert node.ready()
