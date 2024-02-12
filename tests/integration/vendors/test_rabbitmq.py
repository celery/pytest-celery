from __future__ import annotations

import pytest
from kombu import Connection

from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from tests.defaults import ALL_RABBITMQ_FIXTURES


@pytest.fixture
def container(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("container", ALL_RABBITMQ_FIXTURES, indirect=["container"])
class test_rabbitmq_container:
    def test_client(self, container: RabbitMQContainer):
        c: Connection = container.client
        assert c
        try:
            assert c.connect()
        finally:
            c.release()

    def test_celeryconfig(self, container: RabbitMQContainer):
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        config = container.celeryconfig
        assert set(config.keys()) == expected_keys
        assert container.prefix() in config["url"]
        assert container.prefix() in config["host_url"]


class test_rabbitmq_test_broker:
    def test_config(self, celery_rabbitmq_broker: RabbitMQTestBroker):
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        assert set(celery_rabbitmq_broker.config().keys()) == expected_keys
        assert celery_rabbitmq_broker.container.prefix() in celery_rabbitmq_broker.config()["url"]
        assert celery_rabbitmq_broker.container.prefix() in celery_rabbitmq_broker.config()["host_url"]
