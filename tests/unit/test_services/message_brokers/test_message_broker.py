from __future__ import annotations

from unittest.mock import Mock, sentinel

import pytest

from pytest_celery.test_services.message_brokers import MessageBroker


class FakeMessageBroker(MessageBroker):
    @property
    def url(self):
        return sentinel.FAKE_MESSAGE_BROKER_URL

@pytest.fixture
def message_broker(container, test_session_id) -> FakeMessageBroker:
    return FakeMessageBroker(container, test_session_id)


def test_start(message_broker: FakeMessageBroker, container: Mock):
    message_broker.start()

    container.start.assert_called_once_with()


def test_stop(message_broker: FakeMessageBroker, container: Mock):
    message_broker.stop()

    container.stop.assert_called_once_with()


def test_context_manager(message_broker: FakeMessageBroker, container: Mock):
    with message_broker:
        container.start.assert_called_once_with()

    container.stop.assert_called_once_with()
