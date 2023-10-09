from typing import Any

from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryWorkerContainer


class UnitTestContainer(CeleryTestContainer):
    @property
    def client(self) -> Any:
        return self


class UnitWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        return self
