from __future__ import annotations

import pika
from redis.client import Redis
from redis.connection import URL_QUERY_ARGUMENT_PARSERS
from rfc3986.builder import URIBuilder

from pytest_celery.compat import cached_property


class RedisTestServiceMixin:
    @property
    def url(self):
        connection_pool = self.client.connection_pool

        connection_kwargs = connection_pool.connection_kwargs
        username = connection_kwargs.get("username", "")
        password = connection_kwargs.get("password", None)
        host = connection_kwargs.get("host", None)
        port = connection_kwargs.get("port", None)
        location = connection_kwargs.get("db", None)

        querystring = {
            key: connection_kwargs[key] for key in URL_QUERY_ARGUMENT_PARSERS.keys() if key in connection_kwargs
        }

        uri_builder = URIBuilder().add_scheme("redis")
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


class RabbitMQTestServiceMixin:
    def _url(self, scheme):
        username = self._container.RABBITMQ_DEFAULT_USER
        password = self._container.RABBITMQ_DEFAULT_PASS
        host = self._container.get_container_host_ip()
        port = self._container.get_exposed_port(self._container.RABBITMQ_NODE_PORT)

        uri_builder = URIBuilder().add_scheme(scheme)
        if username or password:
            uri_builder = uri_builder.add_credentials(username, password)
        if host:
            uri_builder = uri_builder.add_host(host)
        if port:
            uri_builder = uri_builder.add_port(port)

        return uri_builder.geturl()

    @cached_property
    def get_client(self) -> pika.BlockingConnection:
        return pika.BlockingConnection(self._container.get_connection_params())

    def ping(self) -> None:
        connection = pika.BlockingConnection(self._container.get_connection_params())
        if connection.is_open:
            channel = connection.channel()
            channel.queue_declare(queue="ping")
            channel.basic_publish(exchange="", routing_key="ping", body=b"PING")
