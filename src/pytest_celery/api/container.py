from abc import abstractmethod
from typing import Any

from pytest_docker_tools import wrappers
from pytest_docker_tools.exceptions import ContainerNotReady
from pytest_docker_tools.exceptions import TimeoutError
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import defaults


class CeleryTestContainer(wrappers.Container):
    @abstractmethod
    def client(self, max_tries: int = defaults.DEFAULT_READY_MAX_RETRIES) -> Any:
        return self

    @abstractmethod
    def celeryconfig(self) -> dict:
        raise NotImplementedError("CeleryTestContainer.celeryconfig")

    def ready(self) -> bool:
        max_tries = defaults.DEFAULT_READY_MAX_RETRIES
        tries = 1
        while tries <= max_tries:
            try:
                wait_for_callable(
                    f" Container '{self.name}' is warming up",
                    super().ready,
                    timeout=defaults.DEFAULT_READY_TIMEOUT,
                )
                return True
            except TimeoutError:
                tries += 1

        raise ContainerNotReady(
            self,
            f"Can't get test container to be ready (attempted {tries} times): {self.name}",
        )

    def _full_ready(self, match_log: str = "", check_client: bool = True) -> bool:
        ready = super().ready()
        if ready and match_log:
            ready = ready and match_log in self.logs()
        if ready and check_client:
            wait_for_callable(
                "Waiting for client to be ready",
                self.client,
            )
            ready = ready and self.client() is not None
        return ready
