import pytest
from kombu import Connection
from pytest_lazyfixture import lazy_fixture

from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from pytest_celery import defaults


@pytest.mark.parametrize("container", lazy_fixture(defaults.ALL_RABBITMQ_FIXTURES))
class test_rabbitmq_container:
    def test_client(self, container: RabbitMQContainer):
        c: Connection = container.client
        assert c
        try:
            assert c.connect()
        finally:
            c.release()


@pytest.mark.parametrize("node", [lazy_fixture(defaults.CELERY_RABBITMQ_BROKER)])
class test_rabbitmq_test_broker:
    def test_ready(self, node: RabbitMQTestBroker):
        assert node.ready()
