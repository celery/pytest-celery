from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.test_services.mixins import RabbitMQTestServiceMixin


class RabbitMQBroker(RabbitMQTestServiceMixin, MessageBroker):
    @property
    def url(self):
        return self._url("pyamqp")

    def __repr__(self):
        return f"RabbitMQ Broker <{self.url}>"
