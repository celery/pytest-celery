from __future__ import annotations

import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_RABBITMQ_BROKER
from pytest_celery import RABBITMQ_ENV
from pytest_celery import RABBITMQ_IMAGE
from pytest_celery import RABBITMQ_PORTS
from pytest_celery import RABBITMQ_PREFIX
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker


# from pytest_celery import RabbitMQTestBroker
class test_rabbitmq_container:
    def test_version(self):
        assert RabbitMQContainer.version() == "latest"

    def test_env(self):
        assert RabbitMQContainer.initial_env() == RABBITMQ_ENV

    def test_image(self):
        assert RabbitMQContainer.image() == RABBITMQ_IMAGE

    def test_ports(self):
        assert RabbitMQContainer.ports() == RABBITMQ_PORTS

    def test_prefix(self):
        assert RabbitMQContainer.prefix() == RABBITMQ_PREFIX


@pytest.mark.parametrize("broker", [lazy_fixture(CELERY_RABBITMQ_BROKER)])
class test_rabbitmq_broker_api:
    @pytest.mark.skip(reason="Placeholder")
    def test_placeholder(self, broker: RabbitMQTestBroker):
        # The class RabbitMQTestBroker is currently a placeholder
        # so we don't have any specific tests for it yet.
        # This test suite is pre-configured to test the RabbitMQTestBroker
        # and ready to be used once the class is implemented.
        pass
