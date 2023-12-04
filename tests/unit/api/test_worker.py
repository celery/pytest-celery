from __future__ import annotations

import pytest
from celery import Celery
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_WORKER
from pytest_celery import CELERY_WORKER_CLUSTER
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


@pytest.mark.parametrize("worker", [lazy_fixture(CELERY_WORKER)])
class test_celey_test_worker:
    def test_app(self, worker: CeleryTestWorker, celery_setup_app: Celery):
        assert worker.app is celery_setup_app

    def test_version(self, worker: CeleryTestWorker):
        worker.version
        worker.container.version.assert_called_once()

    def test_log_level(self, worker: CeleryTestWorker):
        worker.log_level
        worker.container.log_level.assert_called_once()

    def test_worker_name(self, worker: CeleryTestWorker):
        worker.worker_name
        worker.container.worker_name.assert_called_once()

    def test_worker_queue(self, worker: CeleryTestWorker):
        worker.worker_queue
        worker.container.worker_queue.assert_called_once()


@pytest.mark.parametrize("cluster", [lazy_fixture(CELERY_WORKER_CLUSTER)])
class test_celery_worker_cluster:
    def test_app(self, cluster: CeleryWorkerCluster, celery_setup_app: Celery):
        for node in cluster:
            assert node.app is celery_setup_app

    def test_versions(self, cluster: CeleryWorkerCluster):
        cluster.versions
        for node in cluster:
            node.container.version.assert_called_once()
