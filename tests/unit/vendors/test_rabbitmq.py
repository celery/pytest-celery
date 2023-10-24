from pytest_celery import RABBITMQ_ENV
from pytest_celery import RABBITMQ_IMAGE
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker


class test_rabbitmq_container:
    def test_version(self):
        assert RabbitMQContainer.version() == "latest"

    def test_env(self):
        assert RabbitMQContainer.env() == RABBITMQ_ENV

    def test_image(self):
        assert RabbitMQContainer.image() == RABBITMQ_IMAGE


class test_rabbitmq_broker_api:
    def test_ready(self, celery_rabbitmq_broker: RabbitMQTestBroker):
        celery_rabbitmq_broker.ready()
        celery_rabbitmq_broker.container.ready.assert_called_once()
