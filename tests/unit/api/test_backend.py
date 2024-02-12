from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery import DEFAULT_WORKER_ENV
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend


class test_celey_test_backend:
    def test_default_config_format(self, celery_backend: CeleryTestBackend):
        assert celery_backend.default_config()["url"] == DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]
        assert celery_backend.default_config()["host_url"] == DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]

    def test_restart_no_app(self, celery_backend: CeleryTestBackend):
        assert celery_backend.app is None
        celery_backend.restart()

    def test_restart_with_app(self, celery_backend: CeleryTestBackend, celery_setup_app: Celery):
        celery_backend._app = celery_setup_app
        assert "result_backend" not in celery_setup_app.conf.changes
        celery_backend.restart()
        assert "result_backend" in celery_setup_app.conf.changes


class test_celery_backend_cluster:
    def test_default_config_format(self, celery_backend_cluster: CeleryBackendCluster):
        assert celery_backend_cluster.default_config()["urls"] == [DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]]
        assert celery_backend_cluster.default_config()["host_urls"] == [DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]]

    class test_disabling_cluster:
        @pytest.fixture
        def celery_backend_cluster(self) -> CeleryBackendCluster:
            return None

        def test_disabling_backend_cluster(
            self,
            celery_backend_cluster: CeleryBackendCluster,
            celery_backend_cluster_config: dict,
        ):
            assert celery_backend_cluster is None
            assert celery_backend_cluster_config is None
