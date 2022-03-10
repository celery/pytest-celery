from __future__ import annotations

from urllib.parse import urljoin
from abc import ABCMeta, abstractmethod
from functools import cached_property

from pytest_celery.test_services import TestService


class Node(metaclass=ABCMeta):
    """
    A node is always instantiated by a MessageBroker (in the future, also by a ResultBackend).
    The node instance provides a vhost, a URL at which to access the MessageBroker.
    """

    def __init__(self, test_service: TestService, vhost_name: str):
        self.vhost_name = vhost_name
        self.test_service = test_service  # MessageBroker or ResultBackend

    def start(self):
        """Spin up a container (or reuse if already exists), returning the vhost for the entity"""
        self.test_service.start()
        self.create_vhost_if_missing()

    def stop(self):
        self.test_service.stop()
        self.destroy_vhost()

    def __enter__(self) -> Node:
        """"""
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """"""

    def create_vhost_if_missing(self):
        if self.should_create_vhost:
            self.create_vhost()

    @abstractmethod
    def create_vhost(self):
        pass

    @abstractmethod
    @property
    def should_create_vhost(self) -> bool:
        pass

    @abstractmethod
    def destroy_vhost(self):
        pass

    @cached_property
    def url(self):
        return urljoin(self.test_service.url, self.vhost_name)
