from __future__ import annotations

from unittest.mock import Mock

import pytest

from pytest_celery.nodes import Node


class FakeNode(Node):
    @property
    def should_create_vhost(self) -> bool:
        pass

    def destroy_vhost(self):
        pass

    def create_vhost(self):
        pass

    def create_vhost_if_missing(self):
        pass


@pytest.fixture
def test_service() -> Mock:
    return Mock()


@pytest.fixture
def vhost_name(faker) -> str:
    return faker.pystr()


@pytest.fixture
def node(test_service: Mock, vhost_name: str) -> FakeNode:
    return FakeNode(test_service, vhost_name)


def test_initialization(node, test_service, vhost_name):
    assert node.vhost_name == vhost_name
    assert node.test_service == test_service


def test_start(node: FakeNode, test_service: Mock, vhost_name: str):
    node.start()

    test_service.start.assert_called_once_with()
    node.create_vhost_if_missing.assert_called_once_with()


@pytest.mark.parametrize('should_create_vhost', [True, False], ids=["Should create vhost", "Should not create vhost"])
def test_create_vhost_if_missing(node: FakeNode, should_create_vhost: bool):
        node.create_vhost_if_missing()
        # todo alter node.should_create_vhost to take value of should_create_vhost
        if should_create_vhost:
            node.create_vhost.assert_called_once_with()



