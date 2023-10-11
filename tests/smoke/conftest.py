from typing import Any
from typing import Tuple
from typing import Type

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


class CeleryLatestWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        return self

    @classmethod
    def version(cls) -> str:
        return ""  # Latest

    @classmethod
    def worker_name(cls) -> str:
        return CeleryWorkerContainer.worker_name() + "-latest"

    @classmethod
    def worker_queue(cls) -> str:
        return CeleryWorkerContainer.worker_queue() + "-latest"


celery_latest_worker_image = build(
    path=WORKER_DOCKERFILE_ROOTDIR,
    tag="pytest-celery/components/worker:celery_latest",
    buildargs=CeleryLatestWorkerContainer.buildargs(),
)


celery_latest_worker_container = container(
    image="{celery_latest_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
    wrapper_class=CeleryLatestWorkerContainer,
    timeout=DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_latest_worker(
    celery_latest_worker_container: CeleryWorkerContainer,
    celery_setup_app: Celery,
) -> CeleryTestWorker:
    worker = CeleryTestWorker(
        celery_latest_worker_container,
        app=celery_setup_app,
    )
    yield worker


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
    path=WORKER_DOCKERFILE_ROOTDIR,
    tag="pytest-celery/components/worker:smoke",
    buildargs=SmokeWorkerContainer.buildargs(),
)


default_worker_container = container(
    image="{smoke_tests_worker_image.id}",  # TODO: Use fixture to avoid defining default_worker_container again
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
    wrapper_class=SmokeWorkerContainer,
    timeout=DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_worker_tasks() -> set:
    from tests import tasks as tests_tasks
    from tests.smoke import tasks as smoke_tasks

    yield {
        tests_tasks,
        smoke_tasks,
    }


@pytest.fixture(
    # Each param item is a list of workers to be used in the cluster
    params=[
        ["celery_setup_worker"],
        ["celery_setup_worker", "celery_latest_worker"],
    ]
)
def celery_worker_cluster(request: pytest.FixtureRequest) -> CeleryWorkerCluster:
    nodes: Tuple[CeleryTestWorker] = [request.getfixturevalue(worker) for worker in request.param]
    cluster = CeleryWorkerCluster(*nodes)
    yield cluster
    cluster.teardown()
