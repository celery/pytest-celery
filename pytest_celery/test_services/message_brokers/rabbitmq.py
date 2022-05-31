from pytest_celery.test_services.mixins import RabbitMQTestServiceMixin
from pytest_celery.test_services.result_backends import ResultBackend


class RabbitMQBroker(RabbitMQTestServiceMixin, ResultBackend):
    @property
    def url(self):
        return self._url("pyampq")

    def __repr__(self):
        return f"RabbitMQ Broker <{self.url}>"
