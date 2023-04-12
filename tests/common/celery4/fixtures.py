import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.common.celery4.api import Celery4TestWorker

celery4_worker_image = build(
    path="tests/common/celery4",
    tag="pytest-celery/components/worker:celery4",
)


@pytest.fixture
def celery4_test_worker(celery4_worker: CeleryWorkerContainer, celery_setup_app: Celery) -> Celery4TestWorker:
    return Celery4TestWorker(
        celery4_worker,
        app=celery_setup_app,
    )


celery4_worker = container(
    image="{celery4_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": {"bind": "/app", "mode": "rw"}},
    wrapper_class=CeleryWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)
