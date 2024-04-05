from __future__ import annotations

from typing import Any

import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


class MyWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        return self

    @classmethod
    def version(cls) -> str:
        return "Celery main branch"

    @classmethod
    def log_level(cls) -> str:
        return "INFO"

    @classmethod
    def worker_name(cls) -> str:
        return "my_worker"

    @classmethod
    def worker_queue(cls) -> str:
        return "myworker"


myworker_image = build(
    path=".",
    dockerfile="tests/myworker/Dockerfile",
    tag="pytest-celery/myworker:example",
    buildargs=MyWorkerContainer.buildargs(),
)


myworker_container = container(
    image="{myworker_image.id}",
    ports=MyWorkerContainer.ports(),
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=MyWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
    command=MyWorkerContainer.command(),
)


@pytest.fixture
def myworker_worker(myworker_container: MyWorkerContainer, celery_setup_app: Celery) -> CeleryTestWorker:
    worker = CeleryTestWorker(myworker_container, app=celery_setup_app)
    yield worker
    worker.teardown()
