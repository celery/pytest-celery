from pytest_celery import RabbitMQContainer
from pytest_celery import defaults


class test_rabbitmq_container:
    def test_client(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.client

    def test_celeryconfig(self, rabbitmq_test_container: RabbitMQContainer):
        expected_keys = {"url", "local_url", "hostname", "port", "vhost"}
        assert set(rabbitmq_test_container.celeryconfig.keys()) == expected_keys

    def test_version(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.version() == "latest"

    def test_env(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.env() == defaults.RABBITMQ_ENV

    def test_image(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.image() == defaults.RABBITMQ_IMAGE
