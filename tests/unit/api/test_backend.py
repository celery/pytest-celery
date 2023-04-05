from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend
from pytest_celery import CeleryTestContainer


class test_celey_test_backend:
    def test_ready(self, unit_tests_container: CeleryTestContainer):
        node = CeleryTestBackend(unit_tests_container)
        assert node.ready()


class test_celery_backend_cluster:
    def test_ready(self, unit_tests_container: CeleryTestContainer, local_test_container: CeleryTestContainer):
        node1 = CeleryTestBackend(unit_tests_container)
        node2 = CeleryTestBackend(local_test_container)
        cluster = CeleryBackendCluster(node1, node2)
        assert cluster.ready()
