
from pytest_celery.test_services.base import TestService
from pytest_celery.test_services.nodes.base import Node


class FakeTestService(TestService):
    def to_node(self) -> Node:
        pass


