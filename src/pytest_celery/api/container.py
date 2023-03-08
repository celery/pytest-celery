from abc import abstractmethod
from typing import Any

from pytest_docker_tools import wrappers


class CeleryTestContainer(wrappers.Container):
    @abstractmethod
    def client(self) -> Any:
        pass
