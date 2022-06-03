from __future__ import annotations

from testcontainers.redis import RedisContainer

from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.test_services.mixins import RedisTestServiceMixin


class RedisBroker(RedisTestServiceMixin, MessageBroker):
    def __init__(self, test_session_id: str, port: int = None, container: RedisContainer = None):
        container = container or RedisContainer(port_to_expose=port or 6379)

        super().__init__(container, test_session_id)

    def __repr__(self):
        return f"Redis Broker <{self.url}>"
