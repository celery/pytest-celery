from pytest_celery.test_services.result_backends import ResultBackend
from pytest_celery.test_services.mixins import RabbitMQTestServiceMixin


class RabbitMQBroker(RabbitMQTestServiceMixin, ResultBackend):
    @property
    def url(self):
        return self._url("rpc")

    def __repr__(self):
        return f"RabbitMQ Broker <{self.url}>"
