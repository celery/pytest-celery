import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_BACKEND
from pytest_celery import CELERY_BACKEND_CLUSTER
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend


@pytest.mark.parametrize("backend", [lazy_fixture(CELERY_BACKEND)])
class test_celey_test_backend:
    def test_app(self, backend: CeleryTestBackend):
        assert backend.app is None


@pytest.mark.parametrize("cluster", [lazy_fixture(CELERY_BACKEND_CLUSTER)])
class test_celery_backend_cluster:
    def test_app(self, cluster: CeleryBackendCluster):
        backend: CeleryTestBackend
        for backend in cluster:
            assert backend.app is None
