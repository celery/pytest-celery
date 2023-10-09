from celery import Celery

from pytest_celery import CeleryTestBackend
from pytest_celery import CeleryTestBroker
from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker


class test_celery_test_setup_unit:
    def test_setup_has_worker_cluster(self, celery_setup: CeleryTestSetup, celery_worker: CeleryTestWorker):
        assert len(celery_setup.worker_cluster) == 1
        assert celery_worker in celery_setup.worker_cluster

    def test_setup_has_broker_cluster(self, celery_setup: CeleryTestSetup, celery_broker: CeleryTestBroker):
        assert len(celery_setup.broker_cluster) == 1
        assert celery_broker in celery_setup.broker_cluster

    def test_setup_has_backend_cluster(self, celery_setup: CeleryTestSetup, celery_backend: CeleryTestBackend):
        assert len(celery_setup.backend_cluster) == 1
        assert celery_backend in celery_setup.backend_cluster

    def test_setup_has_app(self, celery_setup: CeleryTestSetup, celery_setup_app: Celery):
        assert celery_setup.app == celery_setup_app

    def test_setup_has_name(self, celery_setup: CeleryTestSetup):
        assert celery_setup.name()

    def test_setup_config_format(self, celery_setup: CeleryTestSetup, celery_worker_cluster_config: dict):
        expected_format = {"broker_url", "result_backend"}
        assert set(celery_setup.config(celery_worker_cluster_config).keys()) == expected_format

    def test_setup_app(self, celery_setup: CeleryTestSetup):
        assert isinstance(celery_setup.app, Celery)
