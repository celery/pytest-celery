from celery import Celery

from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryTestNode


class test_celery_test_node:
    def test_ready(self, unit_tests_container: CeleryTestContainer):
        node = CeleryTestNode(unit_tests_container)
        assert node.ready()

    def test_app(self, unit_tests_container: CeleryTestContainer):
        expected_app = Celery()
        node = CeleryTestNode(unit_tests_container, expected_app)
        assert node.app is expected_app

    def test_default_config_format(self, unit_tests_container: CeleryTestContainer):
        node = CeleryTestNode(unit_tests_container)
        assert node.default_config() == dict()

    def test_eq_opertor(self, unit_tests_container: CeleryTestContainer):
        node1 = CeleryTestNode(unit_tests_container)
        node2 = CeleryTestNode(unit_tests_container)
        assert node1 == node2
        assert node1 is not node2


class test_celery_test_cluster:
    def test_ready(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
    ):
        node1 = CeleryTestNode(unit_tests_container)
        node2 = CeleryTestNode(local_test_container)
        cluster = CeleryTestCluster(node1, node2)
        assert cluster.ready()

    def test_default_config_format(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
    ):
        node1 = CeleryTestNode(unit_tests_container)
        node2 = CeleryTestNode(local_test_container)
        cluster = CeleryTestCluster(node1, node2)
        assert cluster.default_config() == dict()

    def test_set_nodes(self, unit_tests_container: CeleryTestContainer):
        node1 = CeleryTestNode(unit_tests_container)
        node2 = CeleryTestNode(unit_tests_container)
        cluster = CeleryTestCluster(node1)
        cluster._set_nodes(node2)
        assert cluster[0] == node2

    def test_iter(self, unit_tests_container: CeleryTestContainer):
        node1 = CeleryTestNode(unit_tests_container)
        cluster = CeleryTestCluster(node1)
        assert list(cluster) == [node1]

    def test_len(self, unit_tests_container: CeleryTestContainer):
        node1 = CeleryTestNode(unit_tests_container)
        cluster = CeleryTestCluster(node1)
        assert len(cluster) == 1

    def test_getitem(self, unit_tests_container: CeleryTestContainer):
        node1 = CeleryTestNode(unit_tests_container)
        cluster = CeleryTestCluster(node1)
        assert cluster[0] == node1
