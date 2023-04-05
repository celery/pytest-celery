import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from pytest_celery import defaults


@pytest.mark.parametrize("node", [lazy_fixture(defaults.CELERY_WORKER)])
class test_celey_test_worker:
    def test_ready(self, node: CeleryTestWorker):
        assert node.ready()


@pytest.mark.parametrize("cluster", [lazy_fixture(defaults.CELERY_WORKER_CLUSTER)])
class test_celery_worker_cluster:
    def test_ready(self, cluster: CeleryWorkerCluster):
        assert cluster.ready()
