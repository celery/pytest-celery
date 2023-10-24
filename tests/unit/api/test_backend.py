from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend


class test_celey_test_backend:
    def test_default_config_format(self, celery_backend: CeleryTestBackend):
        expected_format = {"url", "local_url"}
        assert set(celery_backend.default_config().keys()) == expected_format


class test_celery_backend_cluster:
    def test_default_config_format(self, celery_backend_cluster: CeleryBackendCluster):
        expected_format = {"urls", "local_urls"}
        assert set(celery_backend_cluster.default_config().keys()) == expected_format
