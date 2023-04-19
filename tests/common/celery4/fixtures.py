import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.common.celery4.api import Celery4WorkerContainer

celery4_worker_image = build(
    path="tests/common/celery4",
    tag="pytest-celery/components/worker:celery4",
    buildargs={
        "CELERY_VERSION": Celery4WorkerContainer.version(),
        "CELERY_LOG_LEVEL": Celery4WorkerContainer.log_level(),
        "CELERY_WORKER_NAME": Celery4WorkerContainer.worker_name(),
        "CELERY_WORKER_QUEUE": Celery4WorkerContainer.worker_queue(),
    },
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
    worker.ready()
    yield worker


celery4_worker_container = container(
    image="{celery4_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{DEFAULT_NETWORK.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=Celery4WorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)
