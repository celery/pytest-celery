from __future__ import annotations

from typing import Any

import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import DEFAULT_WORKER_CONTAINER_TIMEOUT
from pytest_celery import DEFAULT_WORKER_VOLUME
from pytest_celery import WORKER_DOCKERFILE_ROOTDIR
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from pytest_celery import CeleryWorkerContainer


class Celery4WorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        return self

    @classmethod
    def version(cls) -> str:
        return "4.4.7"

    @classmethod
    def log_level(cls) -> str:
        return "INFO"

    @classmethod
    def worker_name(cls) -> str:
        return "celery4_worker"

    @classmethod
    def worker_queue(cls) -> str:
        return "celery4"


celery4_worker_image = build(
    path=WORKER_DOCKERFILE_ROOTDIR,
    tag="pytest-celery/components/worker:celery4",
    buildargs=Celery4WorkerContainer.buildargs(),
)


celery4_worker_container = container(
    image="{celery4_worker_image.id}",
    ports=fxtr("default_worker_ports"),
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery4WorkerContainer,
    timeout=DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery4_worker(
    celery4_worker_container: CeleryWorkerContainer,
    celery_setup_app: Celery,
) -> CeleryTestWorker:
    worker = CeleryTestWorker(
        celery4_worker_container,
        app=celery_setup_app,
    )
    yield worker


class Celery5WorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        # Overriding the worker container until we have a proper client class
        return self

    @classmethod
    def version(cls) -> str:
        return "5.2.7"

    @classmethod
    def log_level(cls) -> str:
        return "INFO"

    @classmethod
    def worker_queue(cls) -> str:
        return "celery5"


celery5_worker_image = build(
    path=WORKER_DOCKERFILE_ROOTDIR,
    tag="pytest-celery/components/worker:celery5",
    buildargs=Celery5WorkerContainer.buildargs(),
)


@pytest.fixture
def default_worker_container_cls() -> type[CeleryWorkerContainer]:
    return Celery5WorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> type[CeleryWorkerContainer]:
    return Celery5WorkerContainer


default_worker_container = container(
    image="{celery5_worker_image.id}",
    ports=fxtr("default_worker_ports"),
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery5WorkerContainer,
    timeout=DEFAULT_WORKER_CONTAINER_TIMEOUT,
    command=fxtr("default_worker_command"),
)


@pytest.fixture
def celery_worker_cluster(
    celery_worker: CeleryTestWorker,
    celery4_worker: CeleryTestWorker,
) -> CeleryWorkerCluster:
    cluster = CeleryWorkerCluster(
        celery_worker,
        celery4_worker,
    )
    yield cluster
    cluster.teardown()
