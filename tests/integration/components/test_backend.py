import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import defaults
from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.backend.node import CeleryTestBackend


@pytest.mark.parametrize(
    "node",
    [
        lazy_fixture(defaults.CELERY_BACKEND),
        lazy_fixture(defaults.CELERY_SESSION_BACKEND),
    ],
)
class test_celey_test_backend:
    def test_ready(self, node: CeleryTestBackend):
        assert node.ready()


@pytest.mark.parametrize(
    "cluster",
    [
        lazy_fixture(defaults.CELERY_BACKEND_CLUSTER),
        lazy_fixture(defaults.CELERY_SESSION_BACKEND_CLUSTER),
    ],
)
class test_celery_backend_cluster:
    def test_ready(self, cluster: CeleryBackendCluster):
        assert cluster.ready()
