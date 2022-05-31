from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.test_services.mixins import RabbitMQTestServiceMixin


class RabbitMQResultBackend(RabbitMQTestServiceMixin, MessageBroker):
    @property
    def url(self):
        return self._url("rpc")

    def __repr__(self):
        return f"RabbitMQ Result Backend <{self.url}>"
