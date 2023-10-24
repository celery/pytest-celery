import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_BROKER
from pytest_celery import CELERY_BROKER_CLUSTER
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker


@pytest.mark.parametrize("broker", [lazy_fixture(CELERY_BROKER)])
class test_celey_test_broker:
    def test_default_config_format(self, broker: CeleryTestBroker):
        expected_format = {"url", "local_url"}
        assert set(broker.default_config().keys()) == expected_format


@pytest.mark.parametrize("cluster", [lazy_fixture(CELERY_BROKER_CLUSTER)])
class test_celery_broker_cluster:
    def test_default_config_format(self, cluster: CeleryBrokerCluster):
        expected_format = {"urls", "local_urls"}
        assert set(cluster.default_config().keys()) == expected_format
