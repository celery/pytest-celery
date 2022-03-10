from __future__ import annotations

from functools import cached_property
from itertools import count

from kombu import Queue
from redis.client import Redis
from testcontainers.redis import RedisContainer

from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.test_services.nodes import MessageBrokerNode
from pytest_celery.utils.compat import List


class RedisBroker(MessageBroker):
    @property
    def url(self):
        pass

    def __init__(self, test_session_id: str, container=None):
        self._vhost_counter = count()
        container = container or RedisContainer()
        super().__init__(container, test_session_id)

    @property
    def queues(self) -> List[Queue]:
        pass

    @cached_property
    def client(self) -> Redis:
        return self.container.get_client()

    def ping(self) -> None:
        self.client.ping()

    def to_node(self) -> MessageBrokerNode:
        next_vhost = next(self._vhost_counter)
        return MessageBrokerNode(self, vhost_name=next_vhost)

    def __repr__(self):
        # todo add configuration details to repr once they are added to this class
        return f"Redis Broker"
