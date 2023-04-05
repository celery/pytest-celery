from pytest_celery import CeleryWorkerContainer


class test_celery_worker_container:
    def test_client(self, worker_test_container: CeleryWorkerContainer):
        assert worker_test_container.client()
