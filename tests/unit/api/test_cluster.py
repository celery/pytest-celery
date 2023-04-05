from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryTestNode


class test_celery_test_node:
    def test_ready(self, unit_tests_container: CeleryTestContainer):
        node = CeleryTestNode(unit_tests_container)
        assert node.ready()


class test_celery_test_cluster:
    def test_ready(self, unit_tests_container: CeleryTestContainer, local_test_container: CeleryTestContainer):
        node1 = CeleryTestNode(unit_tests_container)
        node2 = CeleryTestNode(local_test_container)
        cluster = CeleryTestCluster(node1, node2)
        assert cluster.ready()
