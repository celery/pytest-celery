from __future__ import annotations

from celery import Celery

from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


class test_celey_test_worker:
    def test_app(self, celery_worker: CeleryTestWorker, celery_setup_app: Celery):
        assert celery_worker.app is celery_setup_app

    def test_version(self, celery_worker: CeleryTestWorker):
        celery_worker.version
        celery_worker.container.version.assert_called_once()

    def test_log_level(self, celery_worker: CeleryTestWorker):
        celery_worker.log_level
        celery_worker.container.log_level.assert_called_once()

    def test_worker_name(self, celery_worker: CeleryTestWorker):
        celery_worker.worker_name
        celery_worker.container.worker_name.assert_called_once()

    def test_worker_queue(self, celery_worker: CeleryTestWorker):
        celery_worker.worker_queue
        celery_worker.container.worker_queue.assert_called_once()


class test_celery_worker_cluster:
    def test_app(self, celery_worker_cluster: CeleryWorkerCluster, celery_setup_app: Celery):
        for node in celery_worker_cluster:
            assert node.app is celery_setup_app

    def test_versions(self, celery_worker_cluster: CeleryWorkerCluster):
        celery_worker_cluster.versions
        for node in celery_worker_cluster:
            node.container.version.assert_called_once()
