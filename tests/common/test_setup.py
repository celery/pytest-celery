from celery import Celery

from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.api.setup import CeleryTestSetup


class shared_celery_test_setup_suite:
    def test_ready(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready()

    def test_worker_is_connected_to_backend(self, celery_setup: CeleryTestSetup):
        backend_urls = [backend.container.celeryconfig["local_url"] for backend in celery_setup.backend_cluster]
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            app: Celery = worker.app
            assert app.backend.as_uri() in backend_urls

    def test_worker_is_connected_to_broker(self, celery_setup: CeleryTestSetup):
        broker_urls = [broker.container.celeryconfig["local_url"] for broker in celery_setup.broker_cluster]
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            app: Celery = worker.app
            assert app.connection().as_uri().replace("guest:**@", "") in broker_urls
