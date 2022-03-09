from unittest.mock import Mock

import pytest

from pytest_celery.test_services.nodes import MessageBrokerNode


class FakeMessageBrokerNode(MessageBrokerNode):
    pass


@pytest.fixture
def message_broker() -> Mock:
    return Mock()


def test_start(message_broker):
    pass


def test_stop(message_broker):
    pass
