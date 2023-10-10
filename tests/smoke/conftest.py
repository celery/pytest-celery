from typing import Any
from typing import Type

import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


@pytest.fixture
def default_worker_tasks() -> set:
    from tests import tasks as tests_tasks
    from tests.smoke import tasks as smoke_tasks

    yield {
        tests_tasks,
        smoke_tasks,
    }


class SmokeWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        # Overriding the worker container until we have a proper client class
        return self

    @classmethod
    def worker_name(cls) -> str:
        return CeleryWorkerContainer.worker_name() + "-smoke-worker"

    @classmethod
    def worker_queue(cls) -> str:
        return CeleryWorkerContainer.worker_queue() + "-smoke-tests-queue"


@pytest.fixture
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return SmokeWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return SmokeWorkerContainer


smoke_tests_worker_image = build(
    path=defaults.WORKER_DOCKERFILE_ROOTDIR,
    tag="pytest-celery/components/worker:smoke",
    buildargs=SmokeWorkerContainer.buildargs(),
)


default_worker_container = container(
    image="{smoke_tests_worker_image.id}",  # TODO: Use fixture to avoid defining default_worker_container again
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=SmokeWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)
