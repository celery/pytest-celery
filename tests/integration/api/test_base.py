import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestNode
from tests.defaults import ALL_CLUSTERS_FIXTURES
from tests.defaults import ALL_NODES_FIXTURES


@pytest.mark.parametrize("node", lazy_fixture(ALL_NODES_FIXTURES))
class test_celery_test_node:
    def test_ready(self, node: CeleryTestNode):
        assert node.ready()


@pytest.mark.parametrize("cluster", lazy_fixture(ALL_CLUSTERS_FIXTURES))
class test_celery_test_cluster:
    def test_ready(self, cluster: CeleryTestCluster):
        assert cluster.ready()
