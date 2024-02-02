from __future__ import annotations

import pytest

from pytest_celery import CELERY_BROKER
from pytest_celery import CELERY_BROKER_CLUSTER
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker


@pytest.mark.parametrize("broker", [CELERY_BROKER])
class test_celery_test_broker:
    def test_app(self, broker: CeleryTestBroker, request):
        broker = request.getfixturevalue(broker)
        assert broker.app is None


@pytest.mark.parametrize("cluster", [CELERY_BROKER_CLUSTER])
class test_celery_broker_cluster:
    def test_app(self, cluster: CeleryBrokerCluster, request):
        cluster = request.getfixturevalue(cluster)
        broker: CeleryTestBroker
        for broker in cluster:
            assert broker.app is None

    def test_config(self, cluster: CeleryBrokerCluster, request):
        cluster = request.getfixturevalue(cluster)
        expected_keys = {"urls", "host_urls"}
        assert set(cluster.config().keys()) == expected_keys
