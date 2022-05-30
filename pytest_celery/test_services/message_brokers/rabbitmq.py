from testcontainers.rabbitmq import RabbitMqContainer

from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.test_services.mixins import RabbitMQTestServiceMixin


class RabbitMQBroker(RabbitMQTestServiceMixin, MessageBroker):
    @property
    def url(self):
        return self._url("pyampq")

    def __repr__(self):
        return f"RabbitMQ Broker <{self.url}>"
