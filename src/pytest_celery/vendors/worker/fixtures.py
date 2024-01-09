# mypy: disable-error-code="misc"

from __future__ import annotations

from types import ModuleType

import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr
from pytest_docker_tools import volume

from pytest_celery.api.worker import CeleryTestWorker
from pytest_celery.vendors.worker.container import CeleryWorkerContainer
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_CONTAINER_TIMEOUT
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_VOLUME
from pytest_celery.vendors.worker.defaults import WORKER_DOCKERFILE_ROOTDIR


@pytest.fixture
def celery_setup_worker(
    default_worker_cls: type[CeleryTestWorker],
    default_worker_container: CeleryWorkerContainer,
    default_worker_app: Celery,
) -> CeleryTestWorker:
    """Creates a CeleryTestWorker instance. Responsible for tearing down the
    node.

    Args:
        default_worker_cls (type[CeleryTestWorker]): Interface class.
        default_worker_container (CeleryWorkerContainer): Instantiated CeleryWorkerContainer.
        default_worker_app (Celery): Celery app instance.
    """
    worker = default_worker_cls(
        container=default_worker_container,
        app=default_worker_app,
    )
    yield worker
    worker.teardown()


@pytest.fixture
def default_worker_cls() -> type[CeleryTestWorker]:
    return CeleryTestWorker


@pytest.fixture
def default_worker_container_cls() -> type[CeleryWorkerContainer]:
    return CeleryWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> type[CeleryWorkerContainer]:
    return CeleryWorkerContainer


default_worker_container = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
    wrapper_class=CeleryWorkerContainer,
    timeout=DEFAULT_WORKER_CONTAINER_TIMEOUT,
)

celery_base_worker_image = build(
    path=WORKER_DOCKERFILE_ROOTDIR,
    tag="pytest-celery/components/worker:default",
    buildargs={
        "CELERY_VERSION": fxtr("default_worker_celery_version"),
        "CELERY_LOG_LEVEL": fxtr("default_worker_celery_log_level"),
        "CELERY_WORKER_NAME": fxtr("default_worker_celery_worker_name"),
        "CELERY_WORKER_QUEUE": fxtr("default_worker_celery_worker_queue"),
    },
)

default_worker_volume = volume(
    initial_content=fxtr("default_worker_initial_content"),
)


@pytest.fixture(scope="session")
def default_worker_celery_version(default_worker_container_session_cls: type[CeleryWorkerContainer]) -> str:
    yield default_worker_container_session_cls.version()


@pytest.fixture(scope="session")
def default_worker_celery_log_level(default_worker_container_session_cls: type[CeleryWorkerContainer]) -> str:
    yield default_worker_container_session_cls.log_level()


@pytest.fixture(scope="session")
def default_worker_celery_worker_name(default_worker_container_session_cls: type[CeleryWorkerContainer]) -> str:
    yield default_worker_container_session_cls.worker_name()


@pytest.fixture(scope="session")
def default_worker_celery_worker_queue(default_worker_container_session_cls: type[CeleryWorkerContainer]) -> str:
    yield default_worker_container_session_cls.worker_queue()


@pytest.fixture
def default_worker_env(
    default_worker_container_cls: type[CeleryWorkerContainer],
    celery_worker_cluster_config: dict,
) -> dict:
    yield default_worker_container_cls.env(celery_worker_cluster_config)


@pytest.fixture
def default_worker_initial_content(
    default_worker_container_cls: type[CeleryWorkerContainer],
    default_worker_app_module: ModuleType,
    default_worker_utils_module: ModuleType,
    default_worker_tasks: set,
    default_worker_signals: set,
    default_worker_app: Celery,
) -> dict:
    yield default_worker_container_cls.initial_content(
        app_module=default_worker_app_module,
        utils_module=default_worker_utils_module,
        worker_tasks=default_worker_tasks,
        worker_signals=default_worker_signals,
        worker_app=default_worker_app,
    )


@pytest.fixture
def default_worker_app_module(default_worker_container_cls: type[CeleryWorkerContainer]) -> ModuleType:
    yield default_worker_container_cls.app_module()


@pytest.fixture
def default_worker_utils_module(default_worker_container_cls: type[CeleryWorkerContainer]) -> ModuleType:
    yield default_worker_container_cls.utils_module()


@pytest.fixture
def default_worker_tasks(default_worker_container_cls: type[CeleryWorkerContainer]) -> set:
    yield default_worker_container_cls.tasks_modules()


@pytest.fixture
def default_worker_signals(default_worker_container_cls: type[CeleryWorkerContainer]) -> set:
    yield default_worker_container_cls.signals_modules()


@pytest.fixture
def default_worker_app(celery_setup_app: Celery) -> Celery:
    yield celery_setup_app
