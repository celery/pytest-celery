"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the :ref:`built-in-worker` vendor.
"""

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
    """Default worker class. Override to apply custom configuration globally.

    See also: :ref:`vendor-class`.

    Returns:
        type[CeleryTestWorker]: API for managing the vendor's node.
    """
    return CeleryTestWorker


@pytest.fixture
def default_worker_container_cls() -> type[CeleryWorkerContainer]:
    """Default worker container class. Override to apply custom configuration
    globally.

    See also: :ref:`vendor-class`.

    Returns:
        type[CeleryWorkerContainer]: API for managing the vendor's container.
    """
    return CeleryWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> type[CeleryWorkerContainer]:
    """Default worker container session class. Override to apply custom
    configuration globally.

    See also: :ref:`vendor-class`.

    Returns:
        type[CeleryWorkerContainer]: API for managing the vendor's container.
    """
    return CeleryWorkerContainer


default_worker_container = container(
    image="{celery_base_worker_image.id}",
    ports=fxtr("default_worker_ports"),
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
    wrapper_class=CeleryWorkerContainer,
    timeout=DEFAULT_WORKER_CONTAINER_TIMEOUT,
    command=fxtr("default_worker_command"),
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
    """Celery version for this worker.

    Args:
        default_worker_container_session_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        str: Celery version.
    """
    return default_worker_container_session_cls.version()


@pytest.fixture(scope="session")
def default_worker_celery_log_level(default_worker_container_session_cls: type[CeleryWorkerContainer]) -> str:
    """Log level for this worker.

    Args:
        default_worker_container_session_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        str: Log level.
    """
    return default_worker_container_session_cls.log_level()


@pytest.fixture(scope="session")
def default_worker_celery_worker_name(default_worker_container_session_cls: type[CeleryWorkerContainer]) -> str:
    """Name of the worker.

    Args:
        default_worker_container_session_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        str: Worker name.
    """
    return default_worker_container_session_cls.worker_name()


@pytest.fixture(scope="session")
def default_worker_celery_worker_queue(default_worker_container_session_cls: type[CeleryWorkerContainer]) -> str:
    """Worker queue for this worker.

    Args:
        default_worker_container_session_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        str: Worker queue.
    """
    return default_worker_container_session_cls.worker_queue()


@pytest.fixture
def default_worker_command(default_worker_container_cls: type[CeleryWorkerContainer]) -> list[str]:
    """Command to run the container.

    Args:
        default_worker_container_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        list[str]: Docker CMD instruction.
    """
    return default_worker_container_cls.command()


@pytest.fixture
def default_worker_env(
    default_worker_container_cls: type[CeleryWorkerContainer],
    celery_worker_cluster_config: dict,
) -> dict:
    """Environment variables for this worker.

    Args:
        default_worker_container_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.
        celery_worker_cluster_config (dict): Broker & Backend clusters configuration.

    Returns:
        dict: Items to pass to the container's environment.
    """
    return default_worker_container_cls.initial_env(celery_worker_cluster_config)


@pytest.fixture
def default_worker_initial_content(
    default_worker_container_cls: type[CeleryWorkerContainer],
    default_worker_app_module: ModuleType,
    default_worker_utils_module: ModuleType,
    default_worker_tasks: set,
    default_worker_signals: set,
    default_worker_app: Celery,
) -> dict:
    """Initial content for this worker's volume.

    This is applied on a worker container when using the following volume configuration:

    .. code-block:: python

        default_worker_container = container(
            ...
            volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
            ...
        )

    .. note::

        More volumes may be added additionally.

    Args:
        default_worker_container_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.
        default_worker_app_module (ModuleType): App module to inject.
        default_worker_utils_module (ModuleType): Utils module to inject.
        default_worker_tasks (set): Tasks modules to inject.
        default_worker_signals (set): Signals modules to inject.
        default_worker_app (Celery): Celery app to initialize the worker with.

    Returns:
        dict: Initial volume content (dict of files).
    """
    return default_worker_container_cls.initial_content(
        app_module=default_worker_app_module,
        utils_module=default_worker_utils_module,
        worker_tasks=default_worker_tasks,
        worker_signals=default_worker_signals,
        worker_app=default_worker_app,
    )


@pytest.fixture
def default_worker_ports(default_worker_container_cls: type[CeleryWorkerContainer]) -> dict | None:
    """Port bindings for this vendor.

    Args:
        default_worker_container_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Port bindings.
    """
    return default_worker_container_cls.ports()


@pytest.fixture
def default_worker_app_module(default_worker_container_cls: type[CeleryWorkerContainer]) -> ModuleType:
    """App module for this worker.

    Args:
        default_worker_container_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        ModuleType: App module.
    """
    return default_worker_container_cls.app_module()


@pytest.fixture
def default_worker_utils_module(default_worker_container_cls: type[CeleryWorkerContainer]) -> ModuleType:
    """Utils module for this worker.

    Args:
        default_worker_container_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        ModuleType: Utils module.
    """
    return default_worker_container_cls.utils_module()


@pytest.fixture
def default_worker_tasks(default_worker_container_cls: type[CeleryWorkerContainer]) -> set:
    """Tasks modules set for this worker.

    Args:
        default_worker_container_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        set: Tasks modules.
    """
    return default_worker_container_cls.tasks_modules()


@pytest.fixture
def default_worker_signals(default_worker_container_cls: type[CeleryWorkerContainer]) -> set:
    """Signals modules set for this worker.

    Args:
        default_worker_container_cls (type[CeleryWorkerContainer]): See also: :ref:`vendor-class`.

    Returns:
        set: Signals modules.
    """
    return default_worker_container_cls.signals_modules()


@pytest.fixture
def default_worker_app(celery_setup_app: Celery) -> Celery:
    """Celery app instance for this worker.

    Args:
        celery_setup_app (Celery): See also: :ref:`vendor-class`.

    Returns:
        Celery: Celery app instance.
    """
    return celery_setup_app
