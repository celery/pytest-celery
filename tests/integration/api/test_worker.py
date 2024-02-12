from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestNode
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from pytest_celery import CeleryWorkerContainer
from tests.integration.api.test_base import BaseCluster
from tests.integration.api.test_base import BaseNodes


class test_celey_test_worker(BaseNodes):
    @pytest.fixture
    def node(self, celery_worker: CeleryTestWorker) -> CeleryTestNode:
        return celery_worker

    def test_app(self, celery_worker: CeleryTestWorker, celery_setup_app: Celery):
        assert celery_worker.app is celery_setup_app

    def test_version(self, celery_worker: CeleryTestWorker):
        assert celery_worker.version == CeleryWorkerContainer.version()

    def test_hostname(self, celery_worker: CeleryTestWorker):
        hostname = celery_worker.hostname()
        assert "@" in hostname
        assert celery_worker.worker_name in hostname.split("@")[0]
        assert celery_worker.container.id[:12] in hostname.split("@")[1]

    def test_wait_for_log(self, celery_worker: CeleryTestWorker):
        log = f"{celery_worker.hostname()} v{celery_worker.version}"
        celery_worker.wait_for_log(log, "test_celey_test_worker.test_wait_for_log")

    def test_assert_log_exists(self, celery_worker: CeleryTestWorker):
        log = f"{celery_worker.hostname()} v{celery_worker.version}"
        celery_worker.assert_log_exists(log, "test_celey_test_worker.test_assert_log_exists")


class test_celery_worker_cluster(BaseCluster):
    @pytest.fixture
    def cluster(self, celery_worker_cluster: CeleryWorkerCluster) -> CeleryTestCluster:
        return celery_worker_cluster

    def test_app(self, celery_worker_cluster: CeleryWorkerCluster, celery_setup_app: Celery):
        worker: CeleryTestWorker
        for worker in celery_worker_cluster:
            assert worker.app is celery_setup_app

    def test_config(self, celery_worker_cluster: CeleryWorkerCluster):
        with pytest.raises(NotImplementedError):
            celery_worker_cluster.config()

    def test_versions(self, celery_worker_cluster: CeleryWorkerCluster):
        assert celery_worker_cluster.versions == {CeleryWorkerContainer.version()}
