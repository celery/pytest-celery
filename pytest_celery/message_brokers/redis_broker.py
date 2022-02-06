from __future__ import annotations

from functools import cached_property
from typing import List

from kombu import Queue
from redis.client import Redis
from testcontainers.redis import RedisContainer

from pytest_celery.message_brokers.message_broker import MessageBroker


class RedisBroker(MessageBroker):
    @property
    def queues(self) -> list[Queue]:
        pass

    def __init__(self, container=None):
        container = container or RedisContainer()
        super().__init__(container)

    @cached_property
    def client(self) -> Redis:
        return self.container.get_client()

    def ping(self) -> None:
        self.client.ping()
