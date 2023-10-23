from celery import Celery

from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


class test_celey_test_worker:
    def test_app(self, unit_tests_container: CeleryTestContainer, celery_setup_app: Celery):
        # TODO: Use mock instead of real container
        node = CeleryTestWorker(unit_tests_container, celery_setup_app)
        assert node.app is celery_setup_app

    def test_version(self, unit_tests_container: CeleryTestContainer, celery_setup_app: Celery):
        # TODO: Use mock instead of real container
        node = CeleryTestWorker(unit_tests_container, celery_setup_app)
        assert node.version == "unknown"


class test_celery_worker_cluster:
    def test_app(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
        celery_setup_app: Celery,
    ):
        # TODO: Use mock instead of real container
        node1 = CeleryTestWorker(unit_tests_container, celery_setup_app)
        node2 = CeleryTestWorker(local_test_container, celery_setup_app)
        cluster = CeleryWorkerCluster(node1, node2)
        node: CeleryTestWorker
        for node in cluster:
            assert node.app is celery_setup_app

    def test_versions(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
        celery_setup_app: Celery,
    ):
        # TODO: Use mock instead of real container
        node1 = CeleryTestWorker(unit_tests_container, celery_setup_app)
        node2 = CeleryTestWorker(local_test_container, celery_setup_app)
        cluster = CeleryWorkerCluster(node1, node2)
        assert cluster.versions == {"unknown"}
