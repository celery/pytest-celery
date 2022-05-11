from __future__ import annotations

from functools import cached_property
from urllib.parse import urlunsplit

from redis.client import Redis
from redis.connection import SSLConnection, UnixDomainSocketConnection
from testcontainers.redis import RedisContainer

from pytest_celery.test_services.message_brokers import MessageBroker


class RedisBroker(MessageBroker):
    def __init__(self, test_session_id: str, port: int = None, container: RedisContainer = None):
        container = container or RedisContainer(port_to_expose=port or 6379)

        super().__init__(container, test_session_id)

    @property
    def url(self):
        connection_pool = self.client.connection_pool
        connection_kwargs = connection_pool.connection_kwargs.copy()
        host = connection_kwargs.pop("host", None)
        return host

    @cached_property
    def client(self) -> Redis:
        return self._container.get_client()

    def ping(self) -> None:
        self.client.ping()

    def __repr__(self):
        # todo add configuration details to repr once they are added to this class
        return f"Redis Broker <port={self._container.port_to_expose}>"
