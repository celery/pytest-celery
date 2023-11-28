from __future__ import annotations

from typing import Any

import pytest_docker_tools
from pytest_docker_tools import wrappers
from pytest_docker_tools.wrappers.container import wait_for_callable
from retry import retry


class CeleryTestContainer(wrappers.Container):
    @property
    def client(self) -> Any:
        raise NotImplementedError("CeleryTestContainer.client")

    @property
    def celeryconfig(self) -> dict:
        raise NotImplementedError("CeleryTestContainer.celeryconfig")

    @classmethod
    def command(cls) -> list:
        # To be used with pytest_docker_tools.container using the command
        # kwarg with the class method as value
        # e.g. command=MyContainer.command()
        raise NotImplementedError("CeleryTestContainer.command")

    def teardown(self) -> None:
        pass

    @property
    def ready_prompt(self) -> str | None:
        return None

    def _wait_port(self, port: str) -> int:
        if not port:
            raise ValueError("Port cannot be empty")

        while not super().ready():
            pass
        _, p = self.get_addr(port)
        return p

    @retry(pytest_docker_tools.exceptions.TimeoutError, delay=10, tries=3)
    def _wait_ready(self, timeout: int = 30) -> bool:
        if self.ready_prompt is not None:
            if self.ready_prompt not in self.logs():
                wait_for_callable(
                    f"Waiting for {self.__class__.__name__}::{self.name} to get ready",
                    lambda: self.ready_prompt in self.logs(),
                    timeout=timeout,
                )

        wait_for_callable(
            f"{self.__class__.__name__}::{self.name} is ready",
            lambda: self.ready_prompt or "" in self.logs(),
        )
        return True

    def ready(self) -> bool:
        if super().ready():
            return self._wait_ready()
        else:
            return False
