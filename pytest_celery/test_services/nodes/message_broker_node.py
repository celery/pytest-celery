# from pytest_celery.test_services.message_brokers.base import MessageBroker
from pytest_celery.test_services.nodes.base import Node


class MessageBrokerNode(Node):

    def __init__(self, message_broker):
        self.message_broker = message_broker

    def start(self) -> str:
        """Starts up a message broker, and returns the URL of the vhost"""
        pass

    def stop(self):
        pass

