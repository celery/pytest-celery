from unittest.mock import Mock

import pytest

from pytest_celery.nodes import MessageBrokerNode


class FakeMessageBrokerNode(MessageBrokerNode):
    def create_vhost(self):
        pass


@pytest.fixture
def message_broker() -> Mock:
    return Mock()


def test_start(message_broker):
    pass


def test_stop(message_broker):
    pass
