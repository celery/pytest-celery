from typing import Any

import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


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
    path="src/pytest_celery/vendors/worker",
    tag="pytest-celery/components/worker:celery4",
    buildargs=Celery4WorkerContainer.buildargs(),
)


celery4_worker_container = container(
    image="{celery4_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery4WorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
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
    path="src/pytest_celery/vendors/worker",
    tag="pytest-celery/components/worker:celery5",
    buildargs=Celery5WorkerContainer.buildargs(),
)
