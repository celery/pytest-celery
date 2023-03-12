import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import defaults
from pytest_celery.api.components.cluster.base import CeleryTestCluster
from pytest_celery.api.components.cluster.node import CeleryTestNode


@pytest.mark.parametrize(
    "node",
    lazy_fixture(defaults.ALL_NODES_FIXTURES),
)
class test_celery_test_node:
    def test_ready(self, node: CeleryTestNode):
        assert node.ready()


@pytest.mark.parametrize(
    "cluster",
    lazy_fixture(defaults.ALL_CLUSTERS_FIXTURES),
)
class test_celery_test_cluster:
    def test_ready(self, cluster: CeleryTestCluster):
        assert cluster.ready()
