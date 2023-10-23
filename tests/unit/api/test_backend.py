from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend
from pytest_celery import CeleryTestContainer


class test_celey_test_backend:
    def test_default_config_format(self, unit_tests_container: CeleryTestContainer):
        # TODO: Use mock instead of real container
        node = CeleryTestBackend(unit_tests_container)
        expected_format = {"url", "local_url"}
        assert set(node.default_config().keys()) == expected_format


class test_celery_backend_cluster:
    def test_default_config_format(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
    ):
        # TODO: Use mock instead of real container
        node1 = CeleryTestBackend(unit_tests_container)
        node2 = CeleryTestBackend(local_test_container)
        cluster = CeleryBackendCluster(node1, node2)
        expected_format = {"urls", "local_urls"}
        assert set(cluster.default_config().keys()) == expected_format
