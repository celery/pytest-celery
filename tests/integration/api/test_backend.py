from __future__ import annotations

import pytest

from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestBackend
from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestNode
from tests.integration.api.test_base import BaseCluster
from tests.integration.api.test_base import BaseNodes


class test_celey_test_backend(BaseNodes):
    @pytest.fixture
    def node(self, celery_backend: CeleryTestBackend) -> CeleryTestNode:
        return celery_backend


class test_celery_backend_cluster(BaseCluster):
    @pytest.fixture
    def cluster(self, celery_backend_cluster: CeleryBackendCluster) -> CeleryTestCluster:
        return celery_backend_cluster
