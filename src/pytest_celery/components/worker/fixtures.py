from typing import Type

import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr
from pytest_docker_tools import volume

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer


@pytest.fixture
def celery_test_worker(default_worker: CeleryWorkerContainer, celery_setup_app: Celery) -> CeleryTestWorker:
    return CeleryTestWorker(
        container=default_worker,
        app=celery_setup_app,
    )


@pytest.fixture
def default_worker_cls() -> Type[CeleryWorkerContainer]:
    return CeleryWorkerContainer


@pytest.fixture(scope="session")
def default_worker_session_cls() -> Type[CeleryWorkerContainer]:
    return CeleryWorkerContainer


default_worker = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": {"bind": "/app", "mode": "rw"}},
    wrapper_class=CeleryWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)

celery_base_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:base",
    buildargs={
        "CELERY_VERSION": fxtr("default_worker_celery_version"),
    },
)

default_worker_volume = volume(
    initial_content=fxtr("default_worker_initial_content"),
)


@pytest.fixture(scope="session")
def default_worker_celery_version(default_worker_session_cls: Type[CeleryWorkerContainer]) -> str:
    return default_worker_session_cls.version()


@pytest.fixture
def default_worker_env(default_worker_cls: Type[CeleryWorkerContainer], celery_worker_cluster_config: dict) -> dict:
    return default_worker_cls.env(celery_worker_cluster_config)


@pytest.fixture
def default_worker_initial_content(
    default_worker_cls: Type[CeleryWorkerContainer],
    default_worker_tasks: set,
) -> dict:
    return default_worker_cls.initial_content(default_worker_tasks)


@pytest.fixture
def default_worker_tasks(default_worker_cls: Type[CeleryWorkerContainer]) -> set:
    return default_worker_cls.tasks_modules()
