from __future__ import annotations

from redis.client import Redis
from redis.connection import URL_QUERY_ARGUMENT_PARSERS, SSLConnection, UnixDomainSocketConnection
from rfc3986.builder import URIBuilder
from testcontainers.redis import RedisContainer

from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.compat import cached_property


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

        connection_kwargs = connection_pool.connection_kwargs
        username = connection_kwargs.get("username", "")
        password = connection_kwargs.get("password", None)
        host = connection_kwargs.get("host", None)
        port = connection_kwargs.get("port", None)
        location = connection_kwargs.get("db", None)

        querystring = {
            key: connection_kwargs[key] for key in URL_QUERY_ARGUMENT_PARSERS.keys() if key in connection_kwargs
        }

        uri_builder = URIBuilder().add_scheme(scheme)
        if username or password:
            uri_builder = uri_builder.add_credentials(username, password)
        if host:
            uri_builder = uri_builder.add_host(host)
        if port:
            uri_builder = uri_builder.add_port(port)
        if location:
            uri_builder = uri_builder.add_path(location)
        if querystring:
            uri_builder = uri_builder.add_query_from(querystring)

        return uri_builder.geturl()

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
