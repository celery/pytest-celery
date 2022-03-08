from __future__ import annotations

from functools import cached_property

from kombu import Queue
from redis.client import Redis
from testcontainers.redis import RedisContainer

from pytest_celery.test_services.message_brokers.base import MessageBroker
from pytest_celery.utils.compat import List


class RedisBroker(MessageBroker):
    @property
    def queues(self) -> List[Queue]:
        pass

    def __init__(self, container=None):
        container = container or RedisContainer()
        super().__init__(container)

    @cached_property
    def client(self) -> Redis:
        return self.container.get_client()

    def ping(self) -> None:
        self.client.ping()

    def __repr__(self):
        # todo add configuration details to repr once they are added to this class
        return f"Redis Broker"
