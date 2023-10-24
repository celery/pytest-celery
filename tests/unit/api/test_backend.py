import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_BACKEND
from pytest_celery import CELERY_BACKEND_CLUSTER
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend


@pytest.mark.parametrize("backend", [lazy_fixture(CELERY_BACKEND)])
class test_celey_test_backend:
    def test_default_config_format(self, backend: CeleryTestBackend):
        expected_format = {"url", "local_url"}
        assert set(backend.default_config().keys()) == expected_format


@pytest.mark.parametrize("cluster", [lazy_fixture(CELERY_BACKEND_CLUSTER)])
class test_celery_backend_cluster:
    def test_default_config_format(self, cluster: CeleryBackendCluster):
        expected_format = {"urls", "local_urls"}
        assert set(cluster.default_config().keys()) == expected_format
