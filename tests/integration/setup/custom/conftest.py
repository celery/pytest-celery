from typing import Any
from typing import Type

import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.common.celery4.fixtures import *  # noqa


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
        return "DEBUG"

    @classmethod
    def worker_queue(cls) -> str:
        return "celery5"


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return Celery5WorkerContainer


celery5_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:celery5",
    buildargs={
        "CELERY_VERSION": Celery5WorkerContainer.version(),
        "CELERY_LOG_LEVEL": Celery5WorkerContainer.log_level(),
        "CELERY_WORKER_NAME": Celery5WorkerContainer.worker_name(),
        "CELERY_WORKER_QUEUE": Celery5WorkerContainer.worker_queue(),
    },
)

default_worker_container = container(
    image="{celery5_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery5WorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_worker_tasks() -> set:
    from tests.common import tasks

    return {tasks}


@pytest.fixture
def celery_worker_cluster(
    celery_worker: CeleryTestWorker,
    celery4_worker: CeleryTestWorker,
) -> CeleryWorkerCluster:
    cluster = CeleryWorkerCluster(
        celery_worker,
        celery4_worker,
    )
    cluster.ready()
    yield cluster
    cluster.teardown()
