from __future__ import annotations

import pytest
from kombu import Connection

from pytest_celery import CELERY_RABBITMQ_BROKER
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from tests.defaults import ALL_RABBITMQ_FIXTURES


@pytest.mark.parametrize("container", ALL_RABBITMQ_FIXTURES)
class test_rabbitmq_container:
    def test_client(self, container: RabbitMQContainer, request):
        container = request.getfixturevalue(container)
        c: Connection = container.client
        assert c
        try:
            assert c.connect()
        finally:
            c.release()

    def test_celeryconfig(self, container: RabbitMQContainer, request):
        container = request.getfixturevalue(container)
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        config = container.celeryconfig
        assert set(config.keys()) == expected_keys
        assert container.prefix() in config["url"]
        assert container.prefix() in config["host_url"]


@pytest.mark.parametrize("broker", [CELERY_RABBITMQ_BROKER])
class test_rabbitmq_test_broker:
    def test_config(self, broker: RabbitMQTestBroker, request):
        broker = request.getfixturevalue(broker)
        expected_keys = {"url", "host_url", "hostname", "port", "vhost"}
        assert set(broker.config().keys()) == expected_keys
        assert broker.container.prefix() in broker.config()["url"]
        assert broker.container.prefix() in broker.config()["host_url"]
