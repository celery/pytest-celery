from __future__ import annotations

import pytest

from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestBroker
from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestNode
from tests.integration.api.test_base import BaseCluster
from tests.integration.api.test_base import BaseNodes


class test_celery_test_broker(BaseNodes):
    @pytest.fixture
    def node(self, celery_broker: CeleryTestBroker) -> CeleryTestNode:
        return celery_broker


class test_celery_broker_cluster(BaseCluster):
    @pytest.fixture
    def cluster(self, celery_broker_cluster: CeleryBrokerCluster) -> CeleryTestCluster:
        return celery_broker_cluster
