from __future__ import annotations

from unittest.mock import Mock

import pytest

from pytest_celery.test_services.nodes import Node


class FakeNode(Node):
    @property
    def should_create_vhost(self) -> bool:
        pass

    def destroy_vhost(self):
        pass

    def create_vhost(self):
        pass


@pytest.fixture
def test_service() -> Mock:
    Mock()


@pytest.fixture
def vhost_name(faker) -> str:
    return faker.pystr()


def test_initialization(test_service, vhost_name):
    node = FakeNode(test_service, vhost_name)

    assert node.vhost_name == vhost_name
    assert node.test_service == test_service
