from __future__ import annotations

from pytest_celery.nodes import Node


class RedisMessageBrokerNode(Node):

    def __init__(self, message_broker, vhost_name: str):
        super().__init__(message_broker, vhost_name)

    def create_vhost(self):
        pass

    @property
    def should_create_vhost(self) -> bool:
        # TODO check if database exists
        pass

    def destroy_vhost(self):
        pass

    def start(self) -> str:
        """Starts up a message broker, and returns the URL of the vhost"""
        pass

    def stop(self):
        pass
