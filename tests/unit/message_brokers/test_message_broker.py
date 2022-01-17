from __future__ import annotations

from unittest.mock import Mock

import pytest
from kombu import Queue

from pytest_celery.healthchecks.connection import ConnectionHealthy
from pytest_celery.healthchecks.disk import DiskSpaceAvailable
from pytest_celery.message_brokers.message_broker import MessageBroker


class FakeMessageBroker(MessageBroker):
    @property
    def queues(self) -> list[Queue]:
        return []


@pytest.fixture()
def container() -> Mock:
    return Mock()


@pytest.fixture()
def healthcheck_scheduler() -> Mock:
    return Mock()


@pytest.fixture()
def message_broker(container, healthcheck_scheduler) -> FakeMessageBroker:
    return FakeMessageBroker(container, healthcheck_scheduler)


@pytest.fixture()
def connection_healthy() -> Mock:
    return Mock()


@pytest.fixture()
def disk_space_available() -> Mock:
    return Mock()


def test_start(message_broker, container, healthcheck_scheduler):
    message_broker.start()

    container.start.assert_called_once_with()
    healthcheck_scheduler.start.assert_called_once_with()


def test_stop(message_broker, container, healthcheck_scheduler):
    message_broker.stop()

    container.stop.assert_called_once_with()
    healthcheck_scheduler.stop.assert_called_once_with()


def test_context_manager(message_broker, container, healthcheck_scheduler):
    with message_broker:
        container.start.assert_called_once_with()
        healthcheck_scheduler.start.assert_called_once_with()

    container.stop.assert_called_once_with()
    healthcheck_scheduler.stop.assert_called_once_with()


def test_check_healthy(message_broker, container, healthcheck_scheduler, connection_healthy, disk_space_available):
    container.check_healthy(connection_healthy, disk_space_available)

    healthcheck_scheduler.add_job.assert_called_once_with(connection_healthy(),
                                                          FakeMessageBroker.SCHEDULER_TRIGGER,
                                                          minutes=FakeMessageBroker.SCHEDULER_INTERVAL_MINUTES)
    healthcheck_scheduler.add_job.assert_called_once_with(disk_space_available(),
                                                          FakeMessageBroker.SCHEDULER_TRIGGER,
                                                          minutes=FakeMessageBroker.SCHEDULER_INTERVAL_MINUTES)
