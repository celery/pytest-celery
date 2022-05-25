from testcontainers.rabbitmq import RabbitMqContainer

from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.test_services.mixins import RabbitMQTestServiceMixin


class RabbitMQBroker(RabbitMQTestServiceMixin, MessageBroker):
    def __init__(self, test_session_id: str, port: int = None, container: RabbitMqContainer = None):
        container = container or RabbitMqContainer(port=port or 5672)
        super().__init__(container, test_session_id)

    @property
    def url(self):
        return self._url("pyampq")

    def __repr__(self):
        return f"RabbitMQ Broker <{self.url}>"