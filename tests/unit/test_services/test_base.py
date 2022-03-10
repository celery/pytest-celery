
import pytest

from pytest_celery.test_services import TestService
from pytest_celery.test_services.nodes import Node


class FakeTestService(TestService):
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    @property
    def url(self):
        pass

    def to_node(self) -> Node:
        pass


def test_name():
    pass

