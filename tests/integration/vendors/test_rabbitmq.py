import pytest
from kombu import Connection
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_RABBITMQ_BROKER
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from tests.defaults import ALL_RABBITMQ_FIXTURES


@pytest.mark.parametrize("container", lazy_fixture(ALL_RABBITMQ_FIXTURES))
class test_rabbitmq_container:
    def test_client(self, container: RabbitMQContainer):
        c: Connection = container.client
        assert c
        try:
            assert c.connect()
        finally:
            c.release()

    def test_celeryconfig(self, container: RabbitMQContainer):
        expected_keys = {"url", "local_url", "hostname", "port", "vhost"}
        assert set(container.celeryconfig.keys()) == expected_keys


@pytest.mark.parametrize("broker", [lazy_fixture(CELERY_RABBITMQ_BROKER)])
class test_rabbitmq_test_broker:
    @pytest.mark.skip("Placeholder")
    def test_placeholder(self, broker: RabbitMQTestBroker):
        broker = broker
