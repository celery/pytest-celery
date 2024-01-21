from __future__ import annotations

import os
from typing import Any

import celery
import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


class DjangoWorkerContainer(CeleryWorkerContainer):
    @property
    def client(self) -> Any:
        return self

    @classmethod
    def version(cls) -> str:
        return celery.__version__

    @classmethod
    def log_level(cls) -> str:
        return "INFO"

    @classmethod
    def worker_name(cls) -> str:
        return "django_tests_worker"

    @classmethod
    def worker_queue(cls) -> str:
        return "celery"


worker_image = build(
    path=".",
    dockerfile="tests/DjangoWorker.Dockerfile",
    tag="pytest-celery/examples/django:example",
    buildargs=DjangoWorkerContainer.buildargs(),
)


default_worker_container = container(
    image="{worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
    volumes={
        # Volume: Worker /app
        "{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME,
        # Mount: source
        os.path.abspath(os.getcwd()): {
            "bind": "/src",
            "mode": "rw",
        },
    },
    wrapper_class=DjangoWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_worker_container_cls() -> type[CeleryWorkerContainer]:
    return DjangoWorkerContainer


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> type[CeleryWorkerContainer]:
    return DjangoWorkerContainer
