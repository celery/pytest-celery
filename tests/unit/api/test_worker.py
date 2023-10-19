from celery import Celery

from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


class test_celey_test_worker:
    def test_ready(self, unit_tests_container: CeleryTestContainer, celery_setup_app: Celery):
        node = CeleryTestWorker(unit_tests_container, celery_setup_app)
        assert node.ready()

    def test_default_config_format(
        self,
        unit_tests_container: CeleryTestContainer,
        celery_setup_app: Celery,
    ):
        node = CeleryTestWorker(unit_tests_container, celery_setup_app)
        assert node.default_config() == dict()

    def test_version(self, unit_tests_container: CeleryTestContainer, celery_setup_app: Celery):
        node = CeleryTestWorker(unit_tests_container, celery_setup_app)
        assert node.version == "unknown"

    def test_wait_for_log(self, unit_tests_container: CeleryTestContainer, celery_setup_app: Celery):
        node = CeleryTestWorker(unit_tests_container, celery_setup_app)
        node.wait_for_log("", "test_celey_test_worker.test_wait_for_log")

    def test_assert_log_exists(self, unit_tests_container: CeleryTestContainer, celery_setup_app: Celery):
        node = CeleryTestWorker(unit_tests_container, celery_setup_app)
        node.assert_log_exists("", "test_celey_test_worker.test_assert_log_exists")


class test_celery_worker_cluster:
    def test_ready(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
        celery_setup_app: Celery,
    ):
        node1 = CeleryTestWorker(unit_tests_container, celery_setup_app)
        node2 = CeleryTestWorker(local_test_container, celery_setup_app)
        cluster = CeleryWorkerCluster(node1, node2)
        assert cluster.ready()

    def test_app(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
        celery_setup_app: Celery,
    ):
        node1 = CeleryTestWorker(unit_tests_container, celery_setup_app)
        node2 = CeleryTestWorker(local_test_container, celery_setup_app)
        cluster = CeleryWorkerCluster(node1, node2)
        node: CeleryTestWorker
        for node in cluster:
            assert node.app is celery_setup_app

    def test_default_config_format(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
        celery_setup_app: Celery,
    ):
        node1 = CeleryTestWorker(unit_tests_container, celery_setup_app)
        node2 = CeleryTestWorker(local_test_container, celery_setup_app)
        cluster = CeleryWorkerCluster(node1, node2)
        assert cluster.default_config() == dict()

    def test_versions(
        self,
        unit_tests_container: CeleryTestContainer,
        local_test_container: CeleryTestContainer,
        celery_setup_app: Celery,
    ):
        node1 = CeleryTestWorker(unit_tests_container, celery_setup_app)
        node2 = CeleryTestWorker(local_test_container, celery_setup_app)
        cluster = CeleryWorkerCluster(node1, node2)
        assert cluster.versions == {"unknown"}
