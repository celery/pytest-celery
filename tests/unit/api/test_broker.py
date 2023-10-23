from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker
from pytest_celery import CeleryTestContainer


class test_celery_test_broker:
    def test_default_config_format(self, unit_tests_container: CeleryTestContainer):
        # TODO: Use mock instead of real container
        node = CeleryTestBroker(unit_tests_container)
        expected_format = {"url", "local_url"}
        assert set(node.default_config().keys()) == expected_format


class test_celery_broker_cluster:
    def test_default_config_format(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
    ):
        # TODO: Use mock instead of real container
        node1 = CeleryTestBroker(unit_tests_container)
        node2 = CeleryTestBroker(local_test_container)
        cluster = CeleryBrokerCluster(node1, node2)
        expected_format = {"urls", "local_urls"}
        assert set(cluster.default_config().keys()) == expected_format
