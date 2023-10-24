from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker


class test_celey_test_broker:
    def test_default_config_format(self, celery_broker: CeleryTestBroker):
        expected_format = {"url", "local_url"}
        assert set(celery_broker.default_config().keys()) == expected_format


class test_celery_broker_cluster:
    def test_default_config_format(self, celery_broker_cluster: CeleryBrokerCluster):
        expected_format = {"urls", "local_urls"}
        assert set(celery_broker_cluster.default_config().keys()) == expected_format
