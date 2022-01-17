from __future__ import annotations

from unittest.mock import Mock

import pytest
from kombu import Queue

from pytest_celery.message_brokers.message_broker import MessageBroker


class FakeMessageBroker(MessageBroker):
    @property
    def queues(self) -> list[Queue]:
        return []


@pytest.fixture(autouse=True)
def container() -> Mock:
    return Mock()


@pytest.fixture(autouse=True)
def message_broker(container) -> FakeMessageBroker:
    return FakeMessageBroker(container)


def test_start():
    message_broker.start()

    container.start.assert_called_once_with()


def test_stop():
    message_broker.stop()

    container.stop.assert_called_once_with()


def test_context_manager():
    with message_broker:
        container.start.assert_called_once_with()

    container.stop.assert_called_once_with()
