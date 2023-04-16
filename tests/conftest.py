from typing import Any
from typing import Type

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.containers.worker import CeleryWorkerContainer
from pytest_celery.utils import cached_property

# Overriding the worker container until we have a proper client class
# to return. This will be applied only to the integration & smoke tests.
# Unit tests have their own worker container.


class WorkerContainer(CeleryWorkerContainer):
    @cached_property
    def client(self) -> Any:
        return self


@pytest.fixture
def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
    return WorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
    return WorkerContainer


default_worker_container = container(
    image="{celery_base_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=WorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)
