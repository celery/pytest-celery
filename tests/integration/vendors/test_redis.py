import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_REDIS_BACKEND
from pytest_celery import CELERY_REDIS_BROKER
from pytest_celery import RedisContainer
from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker
from tests.defaults import ALL_REDIS_FIXTURES


@pytest.mark.parametrize("container", lazy_fixture(ALL_REDIS_FIXTURES))
class test_redis_container:
    def test_client(self, container: RedisContainer):
        assert container.client
        assert container.client.ping()
        assert container.client.set("ready", "1")
        assert container.client.get("ready") == "1"
        assert container.client.delete("ready")


@pytest.mark.parametrize("node", [lazy_fixture(CELERY_REDIS_BACKEND)])
class test_redis_test_backend:
    def test_ready(self, node: RedisTestBackend):
        assert node.ready()


@pytest.mark.parametrize("node", [lazy_fixture(CELERY_REDIS_BROKER)])
class test_redis_test_broker:
    def test_ready(self, node: RedisTestBroker):
        assert node.ready()
