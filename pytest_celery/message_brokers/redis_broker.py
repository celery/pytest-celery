from functools import cached_property
from typing import List

from kombu import Queue
from testcontainers.redis import RedisContainer

from pytest_celery.message_brokers.message_broker import MessageBroker


class RedisBroker(MessageBroker):
    @property
    def queues(self) -> List[Queue]:
        pass

    def __init__(self):
        super().__init__(RedisContainer())

    @cached_property
    def client(self):
        return self.container.get_client()

    def ping(self):
        self.client.ping()



