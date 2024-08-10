from __future__ import annotations

import pytest
from kombu import Connection

from pytest_celery import LocalstackContainer
from pytest_celery import LocalstackTestBroker
from tests.defaults import ALL_LOCALSTACK_FIXTURES


@pytest.fixture
def container(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("container", ALL_LOCALSTACK_FIXTURES, indirect=["container"])
class test_localstack_container:
    def test_client(self, container: LocalstackContainer):
        c: Connection = container.client
        assert c
        try:
            assert c.connect()
        finally:
            c.release()

    def test_celeryconfig(self, container: LocalstackContainer):
        expected_keys = {"url", "host_url", "hostname", "port"}
        config = container.celeryconfig
        assert set(config.keys()) == expected_keys
        assert container.prefix() in config["url"]
        assert container.prefix() in config["host_url"]


class test_localstack_test_broker:
    def test_config(self, celery_localstack_broker: LocalstackTestBroker):
        expected_keys = {"url", "host_url", "hostname", "port"}
        assert set(celery_localstack_broker.config().keys()) == expected_keys
        assert celery_localstack_broker.container.prefix() in celery_localstack_broker.config()["url"]
        assert celery_localstack_broker.container.prefix() in celery_localstack_broker.config()["host_url"]
