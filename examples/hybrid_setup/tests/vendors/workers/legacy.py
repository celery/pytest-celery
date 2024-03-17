import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


class LegacyWorkerContainer(CeleryWorkerContainer):
    @classmethod
    def version(cls) -> str:
        return "4.4.7"

    @classmethod
    def worker_queue(cls) -> str:
        return "legacy"


legacy_worker_image = build(
    path=".",
    dockerfile="tests/vendors/workers/legacy.Dockerfile",
    tag="pytest-celery/examples/hybrid_setup:legacy",
    buildargs=LegacyWorkerContainer.buildargs(),
)


legacy_worker_container = container(
    image="{legacy_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{hybrid_setup_example_network.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=LegacyWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
    command=LegacyWorkerContainer.command(),
)


@pytest.fixture
def legacy_worker(legacy_worker_container: LegacyWorkerContainer, celery_setup_app: Celery) -> CeleryTestWorker:
    worker = CeleryTestWorker(legacy_worker_container, app=celery_setup_app)
    yield worker
    worker.teardown()
