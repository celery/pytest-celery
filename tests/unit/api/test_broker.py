from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery import DEFAULT_WORKER_ENV
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker


class test_celey_test_broker:
    def test_default_config_format(self, celery_broker: CeleryTestBroker):
        assert celery_broker.default_config()["url"] == DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]
        assert celery_broker.default_config()["host_url"] == DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]

    def test_restart_no_app(self, celery_broker: CeleryTestBroker):
        assert celery_broker.app is None
        celery_broker.restart()

    def test_restart_with_app(self, celery_broker: CeleryTestBroker, celery_setup_app: Celery):
        celery_broker._app = celery_setup_app
        assert "broker_url" not in celery_setup_app.conf.changes
        celery_broker.restart()
        assert "broker_url" in celery_setup_app.conf.changes


class test_celery_broker_cluster:
    def test_default_config_format(self, celery_broker_cluster: CeleryBrokerCluster):
        assert celery_broker_cluster.default_config()["urls"] == [DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]]
        assert celery_broker_cluster.default_config()["host_urls"] == [DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]]

    class test_disabling_cluster:
        @pytest.fixture
        def celery_broker_cluster(self) -> CeleryBrokerCluster:
            return None

        def test_disabling_broker_cluster(
            self, celery_broker_cluster: CeleryBrokerCluster, celery_broker_cluster_config: dict
        ):
            assert celery_broker_cluster is None
            assert celery_broker_cluster_config is None
