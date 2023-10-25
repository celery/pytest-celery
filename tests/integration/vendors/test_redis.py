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

    def test_celeryconfig(self, container: RedisContainer):
        expected_keys = {"url", "local_url", "hostname", "port", "vhost"}
        config = container.celeryconfig
        assert set(config.keys()) == expected_keys
        assert container.prefix() in config["url"]
        assert container.prefix() in config["local_url"]


@pytest.mark.parametrize("backend", [lazy_fixture(CELERY_REDIS_BACKEND)])
class test_redis_test_backend:
    def test_config(self, backend: RedisTestBackend):
        expected_keys = {"url", "local_url", "hostname", "port", "vhost"}
        assert set(backend.config().keys()) == expected_keys
        assert backend.container.prefix() in backend.config()["url"]
        assert backend.container.prefix() in backend.config()["local_url"]


@pytest.mark.parametrize("broker", [lazy_fixture(CELERY_REDIS_BROKER)])
class test_redis_test_broker:
    def test_config(self, broker: RedisTestBroker):
        expected_keys = {"url", "local_url", "hostname", "port", "vhost"}
        assert set(broker.config().keys()) == expected_keys
        assert broker.container.prefix() in broker.config()["url"]
        assert broker.container.prefix() in broker.config()["local_url"]
