from typing import Any
from typing import Type

import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


class IntegrationWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        # Overriding the worker container until we have a proper client class
        return self

    @classmethod
    def log_level(cls) -> str:
        return "INFO"

    @classmethod
    def worker_name(cls) -> str:
        return CeleryWorkerContainer.worker_name() + "-integration-worker"

    @classmethod
    def worker_queue(cls) -> str:
        return CeleryWorkerContainer.worker_queue() + "-integration-tests-queue"


@pytest.fixture
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return IntegrationWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return IntegrationWorkerContainer


integration_tests_worker_image = build(
    path="src/pytest_celery/vendors/worker",
    tag="pytest-celery/components/worker:integration",
    buildargs=IntegrationWorkerContainer.buildargs(),
)


default_worker_container = container(
    image="{integration_tests_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=IntegrationWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)
