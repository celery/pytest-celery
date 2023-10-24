from celery import Celery

from pytest_celery import DEFAULT_WORKER_VERSION
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


class test_celey_test_worker:
    def test_ready(self, celery_worker: CeleryTestWorker):
        assert celery_worker.ready()
        celery_worker.container.ready.assert_called_once()


class test_celery_worker_cluster:
    def test_app(self, celery_worker_cluster: CeleryWorkerCluster, celery_setup_app: Celery):
        node: CeleryTestWorker
        for node in celery_worker_cluster:
            assert node.app is celery_setup_app

    def test_versions(self, celery_worker_cluster: CeleryWorkerCluster):
        assert celery_worker_cluster.versions == {DEFAULT_WORKER_VERSION}
