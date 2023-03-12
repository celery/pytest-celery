from itertools import count
from time import sleep

from kombu import Connection

from pytest_celery.api.container import CeleryTestContainer


class RabbitMQContainer(CeleryTestContainer):
    def ready(self) -> bool:
        if super().ready():
            c = self.client()
            if c:
                return True
        return False

    def client(self) -> Connection:
        for tries in count(1):
            if tries > 3:
                break
            try:
                _, port = self.get_addr("5672/tcp")
                c = Connection("pyamqp://", port=port)
                return c
            except IndexError:
                sleep(0.1)
                continue
        else:
            raise RuntimeError("Could not connect to RabbitMQ")
