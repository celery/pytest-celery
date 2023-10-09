from celery import Celery

from pytest_celery import CeleryTestWorker


class test_base_test_worker:
    def test_ready(self, celery_setup_worker: CeleryTestWorker):
        assert celery_setup_worker.ready()

    def test_app(self, celery_setup_worker: CeleryTestWorker, celery_setup_app: Celery):
        assert celery_setup_worker.app is celery_setup_app
