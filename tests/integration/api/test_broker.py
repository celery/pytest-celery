import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker
from tests.defaults import CELERY_BROKER
from tests.defaults import CELERY_BROKER_CLUSTER


@pytest.mark.parametrize("node", [lazy_fixture(CELERY_BROKER)])
class test_celery_test_broker:
    def test_ready(self, node: CeleryTestBroker):
        assert node.ready()

    def test_app(self, node: CeleryTestBroker):
        assert node.app is None


@pytest.mark.parametrize("cluster", [lazy_fixture(CELERY_BROKER_CLUSTER)])
class test_celery_broker_cluster:
    def test_ready(self, cluster: CeleryBrokerCluster):
        assert cluster.ready()
