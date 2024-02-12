from __future__ import annotations

import pytest

from pytest_celery import RedisContainer
from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker
from tests.defaults import ALL_REDIS_FIXTURES


@pytest.fixture
def container(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("container", ALL_REDIS_FIXTURES, indirect=["container"])
class test_redis_container:
    def test_client(self, container: RedisContainer):
        assert container.client
        assert container.client.ping()
        assert container.client.set("ready", "1")
        assert container.client.get("ready") == "1"
        assert container.client.delete("ready")

    def test_celeryconfig(self, container: RedisContainer):
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        config = container.celeryconfig
        assert set(config.keys()) == expected_keys
        assert container.prefix() in config["url"]
        assert container.prefix() in config["host_url"]


class test_redis_test_backend:
    def test_config(self, celery_redis_backend: RedisTestBackend):
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        assert set(celery_redis_backend.config().keys()) == expected_keys
        assert celery_redis_backend.container.prefix() in celery_redis_backend.config()["url"]
        assert celery_redis_backend.container.prefix() in celery_redis_backend.config()["host_url"]


class test_redis_test_broker:
    def test_config(self, celery_redis_broker: RedisTestBroker):
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        assert set(celery_redis_broker.config().keys()) == expected_keys
        assert celery_redis_broker.container.prefix() in celery_redis_broker.config()["url"]
        assert celery_redis_broker.container.prefix() in celery_redis_broker.config()["host_url"]
