import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend
from tests.defaults import CELERY_BACKEND
from tests.defaults import CELERY_BACKEND_CLUSTER


@pytest.mark.parametrize("node", [lazy_fixture(CELERY_BACKEND)])
class test_celey_test_backend:
    def test_app(self, node: CeleryTestBackend):
        assert node.app is None


@pytest.mark.parametrize("cluster", [lazy_fixture(CELERY_BACKEND_CLUSTER)])
class test_celery_backend_cluster:
    def test_app(self, cluster: CeleryBackendCluster):
        node: CeleryTestBackend
        for node in cluster:
            assert node.app is None
