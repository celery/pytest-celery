import pytest
from celery import Celery
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_WORKER
from pytest_celery import CELERY_WORKER_CLUSTER
from pytest_celery import DEFAULT_WORKER_VERSION
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


@pytest.mark.parametrize("worker", [lazy_fixture(CELERY_WORKER)])
class test_celey_test_worker:
    def test_ready(self, worker: CeleryTestWorker):
        assert worker.ready()
        worker.container.ready.assert_called_once()


@pytest.mark.parametrize("cluster", [lazy_fixture(CELERY_WORKER_CLUSTER)])
class test_celery_worker_cluster:
    def test_app(self, cluster: CeleryWorkerCluster, celery_setup_app: Celery):
        node: CeleryTestWorker
        for node in cluster:
            assert node.app is celery_setup_app

    def test_versions(self, cluster: CeleryWorkerCluster):
        assert cluster.versions == {DEFAULT_WORKER_VERSION}
