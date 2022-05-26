from __future__ import annotations

import pika
from rfc3986.builder import URIBuilder

from pytest_celery.compat import cached_property


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
