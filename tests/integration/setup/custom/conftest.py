from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults
from tests.conftest import Celery5WorkerContainer


@pytest.fixture
def default_worker_tasks() -> set:
    from tests import tasks

    return {tasks}


@pytest.fixture
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return Celery5WorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return Celery5WorkerContainer


default_worker_container = container(
    image="{celery5_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery5WorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
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
