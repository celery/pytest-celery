import pytest
from celery import Celery
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker
from pytest_celery import defaults
from tests.tasks import identity


@pytest.fixture
def default_worker_tasks() -> set:
    from tests import tasks

    yield {tasks}


class test_celery_test_setup_integration:
    def test_basic_ready(self, celery_setup: CeleryTestSetup):
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

    def test_log_level(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            wait_for_callable(
                "waiting for worker.log_level in worker.logs()",
                lambda: worker.log_level in worker.logs(),
                timeout=defaults.RESULT_TIMEOUT,
            )

    def test_ready(self, celery_setup: CeleryTestSetup):
        for worker in celery_setup.worker_cluster:
            queue = worker.worker_queue
            r = identity.s("test_ready").apply_async(queue=queue)
            assert r.get(timeout=defaults.RESULT_TIMEOUT) == "test_ready"

    def test_celery_test_setup_ready_ping(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready(ping=True)

    def test_celery_test_setup_ready_ping_false(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready(ping=False)
