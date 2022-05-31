from pytest_celery.test_services.mixins import RabbitMQTestServiceMixin
from pytest_celery.test_services.result_backends import ResultBackend


class RabbitMQResultBackend(RabbitMQTestServiceMixin, ResultBackend):
    @property
    def url(self):
        return self._url("rpc")

    def __repr__(self):
        return f"RabbitMQ Result Backend <{self.url}>"
