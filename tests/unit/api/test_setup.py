from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBackend
from pytest_celery import CeleryTestBroker
from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster


class test_celery_test_setup_unit:
    def test_setup_app(self, celery_setup: CeleryTestSetup):
        assert isinstance(celery_setup.app, Celery)

    def test_setup_has_app(self, celery_setup: CeleryTestSetup, celery_setup_app: Celery):
        assert celery_setup.app == celery_setup_app

    def test_setup_has_backend_cluster(self, celery_setup: CeleryTestSetup, celery_backend: CeleryTestBackend):
        assert len(celery_setup.backend_cluster) == 1
        assert celery_backend in celery_setup.backend_cluster

    def test_setup_has_broker_cluster(self, celery_setup: CeleryTestSetup, celery_broker: CeleryTestBroker):
        assert len(celery_setup.broker_cluster) == 1
        assert celery_broker in celery_setup.broker_cluster

    def test_setup_has_worker_cluster(self, celery_setup: CeleryTestSetup, celery_worker: CeleryTestWorker):
        assert len(celery_setup.worker_cluster) == 1
        assert celery_worker in celery_setup.worker_cluster

    def test_setup_has_name(self, celery_setup: CeleryTestSetup):
        assert celery_setup.name()

    def test_setup_config_format(self, celery_setup: CeleryTestSetup, celery_worker_cluster_config: dict):
        expected_format = {"broker_url", "result_backend"}
        assert set(celery_setup.config(celery_worker_cluster_config).keys()) == expected_format

    def test_update_app_config(self, celery_setup: CeleryTestSetup, celery_setup_app: Celery):
        celery_setup.update_app_config(celery_setup_app)

    def test_create_setup_app(self, celery_setup: CeleryTestSetup, celery_setup_config: dict):
        celery_setup.create_setup_app(celery_setup_config, celery_setup.name())

    def test_create_setup_app_no_config(self, celery_setup: CeleryTestSetup):
        with pytest.raises(ValueError):
            celery_setup.create_setup_app(None, celery_setup.name())

    def test_create_setup_app_no_name(self, celery_setup: CeleryTestSetup, celery_setup_config: dict):
        with pytest.raises(ValueError):
            celery_setup.create_setup_app(celery_setup_config, "")

    def test_teardown(self, celery_setup: CeleryTestSetup):
        celery_setup.teardown()

    @pytest.mark.parametrize(
        "confirmation",
        [
            {"ping": True, "docker": False},
            {"ping": False, "docker": True},
            {"ping": True, "docker": True},
            {"ping": False, "docker": False},
        ],
    )
    def test_ready(self, celery_setup: CeleryTestSetup, confirmation: dict):
        celery_setup.worker_cluster.nodes = tuple()
        assert celery_setup.ready(
            **confirmation,
            control=False,  # Not supported in unit tests
        )

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
