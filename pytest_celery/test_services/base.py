from abc import ABCMeta, abstractmethod
from typing import ContextManager

from pytest_celery.test_services.nodes import Node


class TestService(ContextManager, metaclass=ABCMeta):
    """The test service is responsible for instantiating a node."""

    def __init__(self):
        pass

    def name(self):
        """Name should be a unique ID: <session-id>-<test-service-type>-<config-hash>"""
        pass

    @abstractmethod
    @property
    def url(self):
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def to_node(self) -> Node:
        pass
