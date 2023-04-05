from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker
from pytest_celery import CeleryTestContainer


class test_celery_test_broker:
    def test_ready(self, unit_tests_container: CeleryTestContainer):
        node = CeleryTestBroker(unit_tests_container)
        assert node.ready()


class test_celery_broker_cluster:
    def test_ready(self, unit_tests_container: CeleryTestContainer, local_test_container: CeleryTestContainer):
        node1 = CeleryTestBroker(unit_tests_container)
        node2 = CeleryTestBroker(local_test_container)
        cluster = CeleryBrokerCluster(node1, node2)
        assert cluster.ready()
