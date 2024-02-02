from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery import CELERY_BROKER
from pytest_celery import CELERY_BROKER_CLUSTER
from pytest_celery import DEFAULT_WORKER_ENV
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker


@pytest.mark.parametrize("broker", [CELERY_BROKER])
class test_celey_test_broker:
    def test_default_config_format(self, broker: CeleryTestBroker, request):
        broker = request.getfixturevalue(broker)
        assert broker.default_config()["url"] == DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]
        assert broker.default_config()["host_url"] == DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]

    def test_restart_no_app(self, broker: CeleryTestBroker, request):
        broker = request.getfixturevalue(broker)
        assert broker.app is None
        broker.restart()

    def test_restart_with_app(self, broker: CeleryTestBroker, celery_setup_app: Celery, request):
        broker = request.getfixturevalue(broker)
        broker._app = celery_setup_app
        assert "broker_url" not in celery_setup_app.conf.changes
        broker.restart()
        assert "broker_url" in celery_setup_app.conf.changes


@pytest.mark.parametrize("cluster", [CELERY_BROKER_CLUSTER])
class test_celery_broker_cluster:
    def test_default_config_format(self, cluster: CeleryBrokerCluster, request):
        cluster = request.getfixturevalue(cluster)
        assert cluster.default_config()["urls"] == [DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]]
        assert cluster.default_config()["host_urls"] == [DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]]

    class test_disabling_cluster:
        @pytest.fixture
        def celery_broker_cluster(self) -> CeleryBrokerCluster:
            return None

        def test_disabling_broker_cluster(
            self, cluster: CeleryBrokerCluster, celery_broker_cluster_config: dict, request
        ):
            cluster = request.getfixturevalue(cluster)
            assert cluster is None
            assert celery_broker_cluster_config is None
