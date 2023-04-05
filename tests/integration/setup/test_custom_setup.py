import pytest

from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.api.setup import CeleryTestSetup
from tests.common.celery4.api import Celery4TestWorker
from tests.common.celery4.fixtures import *  # noqa
from tests.common.tasks import identity


@pytest.fixture(scope="session")
def function_worker_celery_version() -> str:
    return "5.2.7"


@pytest.fixture
def function_worker_tasks() -> set:
    from tests.common import tasks

    return {tasks}


@pytest.fixture
def celery_worker_cluster(
    celery_worker: CeleryTestWorker,
    celery4_test_worker: Celery4TestWorker,
) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(
        celery_worker,
        celery4_test_worker,
    )


class test_custom_setup:
    def test_celery_setup_override(self, celery_setup: CeleryTestSetup):
        r1 = identity.s("test_ready").delay()
        r2 = identity.s("test_ready").delay()
        assert r1.get() == "test_ready"
        assert r2.get() == "test_ready"
        assert celery_setup.app

    def test_worker_is_connected_to_backend(self, celery_setup: CeleryTestSetup):
        backend_urls = [backend.container.celeryconfig()["local_url"] for backend in celery_setup.backend_cluster.nodes]
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster.nodes:
            app = worker.app
            assert app.backend.as_uri() in backend_urls

    def test_worker_is_connected_to_broker(self, celery_setup: CeleryTestSetup):
        broker_urls = [broker.container.celeryconfig()["local_url"] for broker in celery_setup.broker_cluster.nodes]
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster.nodes:
            app = worker.app
            assert app.connection().as_uri().replace("guest:**@", "") in broker_urls
