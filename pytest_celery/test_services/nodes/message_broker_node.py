from __future__ import annotations

from pytest_celery.test_services.nodes import Node


class MessageBrokerNode(Node):

    def create_vhost(self):
        pass

    @property
    def should_create_vhost(self) -> bool:
        pass

    def destroy_vhost(self):
        pass

    def __init__(self, message_broker, vhost_name: str):
        super().__init__(message_broker, vhost_name)

    def start(self) -> str:
        """Starts up a message broker, and returns the URL of the vhost"""
        pass

    def stop(self):
        pass

