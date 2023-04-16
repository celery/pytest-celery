from typing import Any

from pytest_celery import CeleryTestContainer
from pytest_celery.containers.worker import CeleryWorkerContainer
from pytest_celery.utils import cached_property


class UnitTestContainer(CeleryTestContainer):
    @cached_property
    def client(self) -> Any:
        return self


class UnitWorkerContainer(CeleryWorkerContainer):
    @cached_property
    def client(self) -> Any:
        return self
