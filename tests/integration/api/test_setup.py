from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from tests.tasks import identity


class test_celery_test_setup_integration:
    @pytest.mark.parametrize(
        "confirmation",
        [
            # Only ping
            {"ping": True, "control": False, "docker": False},
            # Only control
            {"ping": False, "control": True, "docker": False},
            # Only docker
            {"ping": False, "control": False, "docker": True},
            # All
            {"ping": True, "control": True, "docker": True},
        ],
    )
    def test_ready(self, celery_setup: CeleryTestSetup, confirmation: dict):
        assert celery_setup.ready(**confirmation)

    def test_worker_is_connected_to_backend(self, celery_setup: CeleryTestSetup):
        backend_urls = [
            backend.container.celeryconfig["host_url"].replace("cache+", "") for backend in celery_setup.backend_cluster
        ]
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            app: Celery = worker.app
            assert app.backend.as_uri() in backend_urls

    def test_worker_is_connected_to_broker(self, celery_setup: CeleryTestSetup):
        def strip_url(url: str) -> str:
            while url.endswith("/"):
                url = url.rstrip("/")
            return url

        broker_urls = [strip_url(broker.container.celeryconfig["host_url"]) for broker in celery_setup.broker_cluster]
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            app: Celery = worker.app
            as_uri = app.connection().as_uri().replace("guest:**@", "")
            as_uri = strip_url(as_uri)
            assert as_uri in broker_urls

    def test_log_level(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            worker.assert_log_exists(worker.log_level)

    def test_celery_test_setup_ready_ping(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready(ping=True)

    def test_celery_test_setup_ready_ping_false(self, celery_setup: CeleryTestSetup):
        assert celery_setup.ready(ping=False)

    def test_apply_async(self, celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            queue = worker.worker_queue
            r = identity.s("test_ready").apply_async(queue=queue)
            assert r.get(timeout=RESULT_TIMEOUT) == "test_ready"

    class test_disabling_backend_cluster:
        @pytest.fixture
        def celery_backend_cluster(self) -> CeleryBackendCluster:
            return None

        def test_disabling_backend_cluster(self, celery_setup: CeleryTestSetup):
            assert celery_setup.backend_cluster is None
            assert celery_setup.backend is None

    class test_disabling_broker_cluster:
        @pytest.fixture
        def celery_broker_cluster(self) -> CeleryBrokerCluster:
            return None

        @pytest.fixture
        def celery_worker_cluster(self) -> CeleryWorkerCluster:
            return None

        def test_disabling_broker_cluster(self, celery_setup: CeleryTestSetup):
            assert celery_setup.broker_cluster is None
            assert celery_setup.broker is None

    class test_disabling_worker_cluster:
        @pytest.fixture
        def celery_worker_cluster(self) -> CeleryWorkerCluster:
            return None

        def test_disabling_worker_cluster(self, celery_setup: CeleryTestSetup):
            assert celery_setup.worker_cluster is None
            assert celery_setup.worker is None
