from __future__ import annotations

import pytest
import tasks
from celery import Celery
from celery.canvas import Signature
from celery.canvas import group
from celery.result import AsyncResult
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults
from pytest_celery import ping


class GeventWorkerContainer(CeleryWorkerContainer):
    @classmethod
    def command(cls, *args: str) -> list[str]:
        return super().command("-P", "gevent", "-c", "1000")


gevent_worker_image = build(
    path=".",
    dockerfile="Dockerfile",
    tag="pytest-celery/examples/worker_pool:gevent",
    buildargs=GeventWorkerContainer.buildargs(),
)


gevent_worker_container = container(
    image="{gevent_worker_image.id}",
    environment=fxtr("default_worker_env"),
    network="{default_pytest_celery_network.name}",
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


@pytest.fixture
def celery_worker_cluster(gevent_worker: CeleryTestWorker) -> CeleryWorkerCluster:
    cluster = CeleryWorkerCluster(gevent_worker)
    yield cluster
    cluster.teardown()


@pytest.fixture
def default_worker_tasks(default_worker_tasks: set) -> set:
    default_worker_tasks.add(tasks)
    return default_worker_tasks


# ----------------------------


class TestGeventPool:
    def test_celery_banner(self, gevent_worker: CeleryTestWorker):
        gevent_worker.assert_log_exists("concurrency: 1000 (gevent)")

    def test_ping(self, celery_setup: CeleryTestSetup):
        sig: Signature = ping.s()
        res: AsyncResult = sig.apply_async()
        assert res.get(timeout=RESULT_TIMEOUT) == "pong"

    def test_celery_gevent_example(self, celery_setup: CeleryTestSetup):
        """Based on https://github.com/celery/celery/tree/main/examples/gevent"""
        LIST_OF_URLS = [
            "https://github.com/celery",
            "https://github.com/celery/celery",
            "https://github.com/celery/pytest-celery",
        ]
        group(tasks.urlopen.s(url) for url in LIST_OF_URLS).apply_async()
        celery_setup.worker.assert_log_does_not_exist("Exception for")
