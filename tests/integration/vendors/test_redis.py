from __future__ import annotations

import pytest

from pytest_celery import CELERY_REDIS_BACKEND
from pytest_celery import CELERY_REDIS_BROKER
from pytest_celery import RedisContainer
from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker
from tests.defaults import ALL_REDIS_FIXTURES


@pytest.mark.parametrize("container", ALL_REDIS_FIXTURES)
class test_redis_container:
    def test_client(self, container: RedisContainer, request):
        container = request.getfixturevalue(container)
        assert container.client
        assert container.client.ping()
        assert container.client.set("ready", "1")
        assert container.client.get("ready") == "1"
        assert container.client.delete("ready")

    def test_celeryconfig(self, container: RedisContainer, request):
        container = request.getfixturevalue(container)
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        config = container.celeryconfig
        assert set(config.keys()) == expected_keys
        assert container.prefix() in config["url"]
        assert container.prefix() in config["host_url"]


@pytest.mark.parametrize("backend", [CELERY_REDIS_BACKEND])
class test_redis_test_backend:
    def test_config(self, backend: RedisTestBackend, request):
        backend = request.getfixturevalue(backend)
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        assert set(backend.config().keys()) == expected_keys
        assert backend.container.prefix() in backend.config()["url"]
        assert backend.container.prefix() in backend.config()["host_url"]


@pytest.mark.parametrize("broker", [CELERY_REDIS_BROKER])
class test_redis_test_broker:
    def test_config(self, broker: RedisTestBroker, request):
        broker = request.getfixturevalue(broker)
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        assert set(broker.config().keys()) == expected_keys
        assert broker.container.prefix() in broker.config()["url"]
        assert broker.container.prefix() in broker.config()["host_url"]
