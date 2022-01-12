from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import List

from kombu import Queue


class MessageBroker(metaclass=ABCMeta):
    """"""

    def __init__(self, container) -> None:
        self.container = container

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

    @property
    @abstractmethod
    def queues(self) -> list[Queue]:
        pass

    def check_healthy(self):
        pass
