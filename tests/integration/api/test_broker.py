import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker
from pytest_celery import defaults


@pytest.mark.parametrize("node", [lazy_fixture(defaults.CELERY_BROKER)])
class test_celery_test_broker:
    def test_ready(self, node: CeleryTestBroker):
        assert node.ready()


@pytest.mark.parametrize("cluster", [lazy_fixture(defaults.CELERY_BROKER_CLUSTER)])
class test_celery_broker_cluster:
    def test_ready(self, cluster: CeleryBrokerCluster):
        assert cluster.ready()
