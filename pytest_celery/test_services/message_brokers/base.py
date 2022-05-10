from __future__ import annotations

from abc import ABCMeta

from docker.errors import ContainerError

from pytest_celery.test_services import TestService


class MessageBroker(TestService, metaclass=ABCMeta):
    """"""

    def __init__(
            self,
            container,
            test_session_id: str
    ) -> None:
        super().__init__(container, test_session_id)

    def start(self) -> None:
        """"""
        try:
            self._container.start()
        except ContainerError:
            # todo make this specific to the error that a container with the same name is already up and running
            """If a container with the same name (== same configuration) is already up and running, do nothing"""

    def stop(self) -> None:
        """"""
        self._container.stop()
