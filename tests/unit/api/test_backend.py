from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery import CELERY_BACKEND
from pytest_celery import CELERY_BACKEND_CLUSTER
from pytest_celery import DEFAULT_WORKER_ENV
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend


@pytest.mark.parametrize("backend", [CELERY_BACKEND])
class test_celey_test_backend:
    def test_default_config_format(self, request, backend: CeleryTestBackend):
        backend = request.getfixturevalue(backend)
        assert backend.default_config()["url"] == DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]
        assert backend.default_config()["host_url"] == DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]

    def test_restart_no_app(self, request, backend: CeleryTestBackend):
        backend = request.getfixturevalue(backend)
        assert backend.app is None
        backend.restart()

    def test_restart_with_app(self, request, backend: CeleryTestBackend, celery_setup_app: Celery):
        backend = request.getfixturevalue(backend)
        backend._app = celery_setup_app
        assert "result_backend" not in celery_setup_app.conf.changes
        backend.restart()
        assert "result_backend" in celery_setup_app.conf.changes


@pytest.mark.parametrize("cluster", [CELERY_BACKEND_CLUSTER])
class test_celery_backend_cluster:
    def test_default_config_format(self, cluster: CeleryBackendCluster, request):
        cluster = request.getfixturevalue(cluster)
        assert cluster.default_config()["urls"] == [DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]]
        assert cluster.default_config()["host_urls"] == [DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]]

    class test_disabling_cluster:
        @pytest.fixture
        def celery_backend_cluster(self, cluster: CeleryBackendCluster, request) -> CeleryBackendCluster:
            cluster = request.getfixturevalue(cluster)
            return None

        def test_disabling_backend_cluster(
            self, cluster: CeleryBackendCluster, celery_backend_cluster_config: dict, request
        ):
            cluster = request.getfixturevalue(cluster)
            assert cluster is None
            assert celery_backend_cluster_config is None
