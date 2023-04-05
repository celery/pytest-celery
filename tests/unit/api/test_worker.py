from celery import Celery

from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


class test_celey_test_worker:
    def test_ready(self, unit_tests_container: CeleryTestContainer, celery_setup_app: Celery):
        node = CeleryTestWorker(unit_tests_container, celery_setup_app)
        assert node.ready()


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
