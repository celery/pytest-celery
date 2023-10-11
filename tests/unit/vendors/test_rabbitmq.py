from pytest_celery import RABBITMQ_ENV
from pytest_celery import RABBITMQ_IMAGE
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker


class test_rabbitmq_container:
    def test_client(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.client

    def test_celeryconfig(self, rabbitmq_test_container: RabbitMQContainer):
        expected_keys = {"url", "local_url", "hostname", "port", "vhost"}
        assert set(rabbitmq_test_container.celeryconfig.keys()) == expected_keys

    def test_version(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.version() == "latest"

    def test_env(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.env() == RABBITMQ_ENV

    def test_image(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.image() == RABBITMQ_IMAGE


class test_rabbitmq_test_broker:
    def test_ready(self, celery_rabbitmq_broker: RabbitMQTestBroker):
        assert celery_rabbitmq_broker.ready()
