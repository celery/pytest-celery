import json
import urllib.request

import pika
from rfc3986.builder import URIBuilder
from testcontainers.rabbitmq import RabbitMqContainer

from pytest_celery.compat import cached_property


class RabbitMQTestServiceMixin:
    RABBITMQ_MANAGEMENT_NODE_PORT = 15672
    IMAGE_NAME = "rabbitmq:3.10-management"
    PING_ENDPOINT = ""

    def __init__(self, test_session_id: str, port: int = None, container: RabbitMqContainer = None):
        container = container or RabbitMqContainer(image=self.IMAGE_NAME, port=port or 5672)
        container.with_exposed_ports(self.RABBITMQ_MANAGEMENT_NODE_PORT)

        super().__init__(container, test_session_id)

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
        username = self._container.RABBITMQ_DEFAULT_USER
        password = self._container.RABBITMQ_DEFAULT_PASS
        host = self._container.get_container_host_ip()
        port = self._container.get_exposed_port(self.RABBITMQ_MANAGEMENT_NODE_PORT)

        uri_builder = URIBuilder().add_scheme("http")
        if host:
            uri_builder = uri_builder.add_host(host)
        if port:
            uri_builder = uri_builder.add_port(port)
        uri_builder = uri_builder.add_path("api/aliveness-test/%2F")
        url = uri_builder.geturl()

        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()

        p.add_password(None, url, username, password)

        handler = urllib.request.HTTPBasicAuthHandler(p)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        f = urllib.request.urlopen(url)
        status = json.loads(f.read().decode("utf-8"))["status"]
        if status != "ok":
            raise ValueError(f"Status is {status}")
