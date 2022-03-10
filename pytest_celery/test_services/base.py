from __future__ import annotations

from abc import ABCMeta, abstractmethod
from functools import cached_property
from typing import ContextManager


class TestService(ContextManager, metaclass=ABCMeta):
    """The test service is responsible for instantiating a node."""

    def __init__(self, container, test_session_id: str):
        # TODO: Decide if we should rename this attribute
        self.__test_session_id = test_session_id
        self._container = container.with_name(self.name)

    @cached_property
    def name(self) -> str:
        """Name should be a unique ID: <session-id>-<test-service-type>-<config-hash>"""
        return "bla"

    @property
    def test_session_id(self):
        return self.__test_session_id

    @property
    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def to_node(self):
        pass

    def __enter__(self):
        """"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """"""
        self.stop()
