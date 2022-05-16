from __future__ import annotations

from testcontainers.rabbitmq import RabbitMqContainer

from pytest_celery.test_services.message_brokers import MessageBroker
from tests.unit.test_services.message_brokers.utils import create_url


class RabbitMQBroker(MessageBroker):
    def __init__(self, test_session_id: str, port: int = None, container: RabbitMqContainer = None):
        container = container or RabbitMqContainer(port=port or 5672)
        super().__init__(container, test_session_id)

    @property
    def url(self):
        username = self._container.RABBITMQ_DEFAULT_USER
        password = self._container.RABBITMQ_DEFAULT_PASS
        host = self._container.get_container_host_ip()
        port = self._container.get_exposed_port(self._container.RABBITMQ_NODE_PORT)
        return create_url("pyamqp", username, password, host, port)

    def __repr__(self):
        # todo add configuration details to repr once they are added to this class
        return f"RabbitMQ Broker <port={self._container.RABBITMQ_NODE_PORT}>"
