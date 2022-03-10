from __future__ import annotations

from abc import ABCMeta, abstractmethod

from apscheduler.schedulers.background import BackgroundScheduler
from docker.errors import ContainerError
from kombu import Queue

from pytest_celery.healthchecks.connection import ConnectionHealthy
from pytest_celery.healthchecks.disk import DiskSpaceAvailable
from pytest_celery.test_services.base import TestService
from pytest_celery.test_services.nodes.base import Node
from pytest_celery.test_services.nodes.message_broker_node import MessageBrokerNode


class MessageBroker(TestService, metaclass=ABCMeta):
    """"""

    SCHEDULER_TRIGGER = "interval"
    SCHEDULER_INTERVAL_MINUTES = 1

    def __init__(self, container, healthcheck_scheduler=BackgroundScheduler()) -> None:
        self.container = container
        self.healthcheck_scheduler = healthcheck_scheduler

        super().__init__()

    def start(self) -> None:
        """"""
        try:
            self.container.start()
        except ContainerError:
            # todo make this specific to the error that a container with the same name is already up and running
            """If a container with the same name (== same configuration) is already up and running, do nothing"""
            pass
        self.healthcheck_scheduler.start()

    def stop(self) -> None:
        """"""
        self.container.stop()
        self.healthcheck_scheduler.shutdown()

    def __enter__(self) -> MessageBroker:
        """"""
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """"""
        self.stop()

    def check_healthy(self, connection_healthy: ConnectionHealthy, disk_space_available: DiskSpaceAvailable) -> None:
        self.healthcheck_scheduler.add_job(
            connection_healthy(), trigger=self.SCHEDULER_TRIGGER, minutes=self.SCHEDULER_INTERVAL_MINUTES
        )
        self.healthcheck_scheduler.add_job(
            disk_space_available(), trigger=self.SCHEDULER_TRIGGER, minutes=self.SCHEDULER_INTERVAL_MINUTES
        )

    @property
    @abstractmethod
    def queues(self) -> list[Queue]:
        pass
