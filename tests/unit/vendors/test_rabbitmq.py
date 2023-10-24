import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_RABBITMQ_BROKER
from pytest_celery import RABBITMQ_ENV
from pytest_celery import RABBITMQ_IMAGE
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker


# from pytest_celery import RabbitMQTestBroker
class test_rabbitmq_container:
    def test_version(self):
        assert RabbitMQContainer.version() == "latest"

    def test_env(self):
        assert RabbitMQContainer.env() == RABBITMQ_ENV

    def test_image(self):
        assert RabbitMQContainer.image() == RABBITMQ_IMAGE


@pytest.mark.parametrize("broker", [lazy_fixture(CELERY_RABBITMQ_BROKER)])
class test_rabbitmq_broker_api:
    def test_ready(self, broker: RabbitMQTestBroker):
        broker.ready()
        broker.container.ready.assert_called_once()
