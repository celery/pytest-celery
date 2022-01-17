from __future__ import annotations

from abc import ABCMeta, abstractmethod

from apscheduler.schedulers.background import BackgroundScheduler
from kombu import Queue


class MessageBroker(metaclass=ABCMeta):
    """"""

    def __init__(self, container, healthcheck_scheduler=BackgroundScheduler()) -> None:
        self.container = container
        self.healthcheck_scheduler = healthcheck_scheduler

    def start(self) -> None:
        """"""
        self.container.start()

    def stop(self) -> None:
        """"""
        self.container.stop()

    def __enter__(self) -> MessageBroker:
        """"""
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """"""
        self.stop()

    def check_healthy(self) -> None:
        pass

    @property
    @abstractmethod
    def queues(self) -> list[Queue]:
        pass

