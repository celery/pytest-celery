from __future__ import annotations

try:
    from functools import cached_property
except ImportError:
    # TODO: Remove this backport once we drop Python 3.7 support
    from cached_property import cached_property

from redis.client import Redis
from redis.connection import SSLConnection, UnixDomainSocketConnection
from testcontainers.redis import RedisContainer

from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.test_services.message_brokers.utils import create_url


class RedisTestServiceMixin:
    @property
    def url(self):
        connection_pool = self.client.connection_pool
        connection_class = connection_pool.connection_class
        if isinstance(connection_class, SSLConnection):
            scheme = "rediss"
        elif isinstance(connection_class, UnixDomainSocketConnection):
            scheme = "unix"
        else:
            scheme = "redis"

        connection_kwargs = connection_pool.connection_kwargs.copy()
        username = connection_kwargs.pop("username", "")
        password = connection_kwargs.pop("password", "")
        host = connection_kwargs.pop("host", "")
        port = connection_kwargs.pop("port", "")

        return create_url(scheme, username, password, host, port)

    @cached_property
    def client(self) -> Redis:
        return self._container.get_client()

    def ping(self) -> None:
        self.client.ping()


class RedisBroker(RedisTestServiceMixin, MessageBroker):
    def __init__(self, test_session_id: str, port: int = None, container: RedisContainer = None):
        container = container or RedisContainer(port_to_expose=port or 6379)

        super().__init__(container, test_session_id)

    def __repr__(self):
        return f"Redis Broker <{self.url}>"
