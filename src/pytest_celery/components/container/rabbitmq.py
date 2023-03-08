from kombu import Connection

from pytest_celery.api.container import CeleryTestContainer


class RabbitMQContainer(CeleryTestContainer):
    def client(self) -> Connection:
        port = self.get_addr("5672/tcp")[1]
        c = Connection("pyamqp://", port=port)
        return c
