import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


class GeventWorkerContainer(CeleryWorkerContainer):
    @classmethod
    def command(cls, *args: str) -> list[str]:
        return super().command("-P", "gevent", "-c", "1000")


gevent_worker_image = build(
    path=".",
    dockerfile="tests/vendors/workers/gevent.Dockerfile",
    tag="pytest-celery/examples/hybrid_setup:gevent",
    buildargs=GeventWorkerContainer.buildargs(),
)


gevent_worker_container = container(
    image="{gevent_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{hybrid_setup_example_network.name}",
    volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
    wrapper_class=GeventWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
    command=GeventWorkerContainer.command(),
)


@pytest.fixture
def gevent_worker(gevent_worker_container: GeventWorkerContainer, celery_setup_app: Celery) -> CeleryTestWorker:
    worker = CeleryTestWorker(gevent_worker_container, app=celery_setup_app)
    yield worker
    worker.teardown()
