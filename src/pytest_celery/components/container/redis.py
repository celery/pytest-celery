from itertools import count
from time import sleep

from redis import Redis

from pytest_celery.api.container import CeleryTestContainer


class RedisContainer(CeleryTestContainer):
    def ready(self) -> bool:
        if super().ready():
            c = self.client()
            if c.ping():
                return True
        return False

    def client(self) -> Redis:
        while count(3):
            try:
                port = self.get_addr("6379/tcp")[1]
                c = Redis(host="localhost", port=port, db=0, decode_responses=True)
                return c
            except IndexError:
                sleep(0.1)
                continue
        raise RuntimeError("Could not connect to redis")
