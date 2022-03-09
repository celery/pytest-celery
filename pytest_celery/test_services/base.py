from abc import ABCMeta, abstractmethod

from pytest_celery.test_services.nodes.base import Node


class TestService(metaclass=ABCMeta):
    """The test service is responsible for instantiating a node."""

    def __init__(self):
        pass

    @abstractmethod
    def to_node(self) -> Node:
        raise NotImplementedError
