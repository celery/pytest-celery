from __future__ import annotations

from typing import Any

import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import DEFAULT_WORKER_CONTAINER_TIMEOUT
from pytest_celery import DEFAULT_WORKER_VOLUME
from pytest_celery import WORKER_DOCKERFILE_ROOTDIR
from pytest_celery import CeleryWorkerContainer


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
def default_worker_container_cls() -> type[CeleryWorkerContainer]:
    return IntegrationWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> type[CeleryWorkerContainer]:
    return IntegrationWorkerContainer


integration_tests_worker_image = build(
    path=WORKER_DOCKERFILE_ROOTDIR,
    tag="pytest-celery/components/worker:integration",
    buildargs=IntegrationWorkerContainer.buildargs(),
)


default_worker_container = container(
    image="{integration_tests_worker_image.id}",
    ports=fxtr("default_worker_ports"),
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
    wrapper_class=IntegrationWorkerContainer,
    timeout=DEFAULT_WORKER_CONTAINER_TIMEOUT,
    command=fxtr("default_worker_command"),
)
