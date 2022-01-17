from __future__ import annotations

from abc import ABCMeta, abstractmethod

from apscheduler.schedulers.background import BackgroundScheduler
from kombu import Queue

from pytest_celery.healthchecks.connection import ConnectionHealthy
from pytest_celery.healthchecks.disk import DiskSpaceAvailable


class MessageBroker(metaclass=ABCMeta):
    """"""
    SCHEDULER_TRIGGER = 'interval'
    SCHEDULER_INTERVAL_MINUTES = 1

    def __init__(self, container, healthcheck_scheduler=BackgroundScheduler()) -> None:
        self.container = container
        self.healthcheck_scheduler = healthcheck_scheduler

    def start(self) -> None:
        """"""
        self.container.start()
        self.healthcheck_scheduler.start()

    def stop(self) -> None:
        """"""
        self.container.stop()
        self.healthcheck_scheduler.stop()

    def __enter__(self) -> MessageBroker:
        """"""
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """"""
        self.stop()

    def check_healthy(self, connection_healthy: ConnectionHealthy, disk_space_available: DiskSpaceAvailable) -> None:
        pass

    @property
    @abstractmethod
    def queues(self) -> list[Queue]:
        pass

