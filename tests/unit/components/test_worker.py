from pytest_celery.api.components.worker.node import CeleryTestWorker


class test_base_test_worker:
    def test_ready(self, celery_test_worker: CeleryTestWorker):
        assert celery_test_worker.ready()
