from __future__ import annotations

from unittest.mock import Mock, call

import pytest
from apscheduler.schedulers.background import BackgroundScheduler
from kombu import Queue

from pytest_celery.healthchecks.connection import ConnectionHealthy
from pytest_celery.healthchecks.disk import DiskSpaceAvailable
from pytest_celery.message_brokers.message_broker import MessageBroker


class FakeMessageBroker(MessageBroker):
    @property
    def queues(self) -> list[Queue]:
        return []


@pytest.fixture
def container() -> Mock:
    return Mock()


@pytest.fixture
def healthcheck_scheduler() -> Mock:
    return Mock()


@pytest.fixture
def message_broker(container, healthcheck_scheduler) -> FakeMessageBroker:
    return FakeMessageBroker(container, healthcheck_scheduler)


@pytest.fixture
def connection_healthy() -> Mock:
    return Mock()


@pytest.fixture
def disk_space_available() -> Mock:
    return Mock()


def test_start(message_broker: FakeMessageBroker, container: Mock, healthcheck_scheduler: BackgroundScheduler):
    message_broker.start()

    container.start.assert_called_once_with()
    healthcheck_scheduler.start.assert_called_once_with()


def test_stop(message_broker: FakeMessageBroker, container: Mock, healthcheck_scheduler: BackgroundScheduler):
    message_broker.stop()

    container.stop.assert_called_once_with()
    healthcheck_scheduler.shutdown.assert_called_once_with()


def test_context_manager(message_broker: FakeMessageBroker, container: Mock, healthcheck_scheduler: BackgroundScheduler):
    with message_broker:
        container.start.assert_called_once_with()
        healthcheck_scheduler.start.assert_called_once_with()

    container.stop.assert_called_once_with()
    healthcheck_scheduler.shutdown.assert_called_once_with()


def test_check_healthy(message_broker: FakeMessageBroker, container: Mock, healthcheck_scheduler: BackgroundScheduler,
                       connection_healthy: ConnectionHealthy, disk_space_available: DiskSpaceAvailable):
    message_broker.check_healthy(connection_healthy, disk_space_available)

    # todo use trigger and minutes constants from MessageBroker
    call_connection_healthy = call(connection_healthy(), trigger="interval", minutes=1)
    call_disk_space_available = call(disk_space_available(), trigger="interval", minutes=1)

    healthcheck_scheduler.add_job.assert_has_calls([call_connection_healthy, call_disk_space_available])
