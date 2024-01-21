from __future__ import annotations

from celery import Celery

from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker
from tests.integration.api.custom_setup.conftest import Celery4WorkerContainer
from tests.integration.api.custom_setup.conftest import Celery5WorkerContainer
from tests.tasks import identity


class test_custom_setup:
    def test_ready(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready()

    def test_worker_is_connected_to_backend(self, celery_setup: CeleryTestSetup):
        backend_urls = [
            backend.container.celeryconfig["host_url"].replace("cache+", "") for backend in celery_setup.backend_cluster
        ]
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            app: Celery = worker.app
            assert app.backend.as_uri() in backend_urls

    def test_worker_is_connected_to_broker(self, celery_setup: CeleryTestSetup):
        broker_urls = [broker.container.celeryconfig["host_url"] for broker in celery_setup.broker_cluster]
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            app: Celery = worker.app
            assert app.connection().as_uri().replace("guest:**@", "") in broker_urls

    def test_log_level(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            if worker.logs():
                worker.assert_log_exists(worker.log_level)

    def test_apply_async(self, celery_setup: CeleryTestSetup):
        assert celery_setup.app
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            expected = "test_apply_async"
            queue = worker.worker_queue
            sig = identity.s(expected)
            res = sig.apply_async(queue=queue)
            assert res.get(timeout=RESULT_TIMEOUT) == expected

    def test_custom_cluster_version(self, celery_setup: CeleryTestSetup):
        assert len(celery_setup.worker_cluster) == 2
        assert celery_setup.worker_cluster.versions == {
            Celery5WorkerContainer.version(),
            Celery4WorkerContainer.version(),
        }
