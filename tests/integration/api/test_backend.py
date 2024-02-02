from __future__ import annotations

import pytest

from pytest_celery import CELERY_BACKEND
from pytest_celery import CELERY_BACKEND_CLUSTER
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend


@pytest.mark.parametrize("backend", [CELERY_BACKEND])
class test_celey_test_backend:
    def test_app(self, backend: CeleryTestBackend, request):
        backend = request.getfixturevalue(backend)
        assert backend.app is None


@pytest.mark.parametrize("cluster", [CELERY_BACKEND_CLUSTER])
class test_celery_backend_cluster:
    def test_app(self, cluster: CeleryBackendCluster, request):
        cluster = request.getfixturevalue(cluster)
        backend: CeleryTestBackend
        for backend in cluster:
            assert backend.app is None

    def test_config(self, cluster: CeleryBackendCluster, request):
        cluster = request.getfixturevalue(cluster)
        expected_keys = {"urls", "host_urls"}
        assert set(cluster.config().keys()) == expected_keys
