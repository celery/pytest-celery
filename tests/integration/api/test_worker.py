from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery import CELERY_WORKER
from pytest_celery import CELERY_WORKER_CLUSTER
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from pytest_celery import CeleryWorkerContainer


@pytest.mark.parametrize("worker", [CELERY_WORKER])
class test_celey_test_worker:
    def test_app(self, worker: CeleryTestWorker, celery_setup_app: Celery, request):
        worker = request.getfixturevalue(worker)
        assert worker.app is celery_setup_app

    def test_version(self, worker: CeleryTestWorker, request):
        worker = request.getfixturevalue(worker)
        assert worker.version == CeleryWorkerContainer.version()

    def test_hostname(self, worker: CeleryTestWorker, request):
        worker = request.getfixturevalue(worker)
        hostname = worker.hostname()
        assert "@" in hostname
        assert worker.worker_name in hostname.split("@")[0]
        assert worker.container.id[:12] in hostname.split("@")[1]

    def test_wait_for_log(self, worker: CeleryTestWorker, request):
        worker = request.getfixturevalue(worker)
        log = f"{worker.hostname()} v{worker.version}"
        worker.wait_for_log(log, "test_celey_test_worker.test_wait_for_log")

    def test_assert_log_exists(self, worker: CeleryTestWorker, request):
        worker = request.getfixturevalue(worker)
        log = f"{worker.hostname()} v{worker.version}"
        worker.assert_log_exists(log, "test_celey_test_worker.test_assert_log_exists")


@pytest.mark.parametrize("cluster", [CELERY_WORKER_CLUSTER])
class test_celery_worker_cluster:
    def test_app(self, cluster: CeleryWorkerCluster, celery_setup_app: Celery, request):
        cluster = request.getfixturevalue(cluster)
        worker: CeleryTestWorker
        for worker in cluster:
            assert worker.app is celery_setup_app

    def test_config(self, cluster: CeleryWorkerCluster, request):
        cluster = request.getfixturevalue(cluster)
        with pytest.raises(NotImplementedError):
            cluster.config()

    def test_versions(self, cluster: CeleryWorkerCluster, request):
        cluster = request.getfixturevalue(cluster)
        assert cluster.versions == {CeleryWorkerContainer.version()}
