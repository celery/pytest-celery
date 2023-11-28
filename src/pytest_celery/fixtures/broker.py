# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest

from pytest_celery.api.broker import CeleryBrokerCluster
from pytest_celery.api.broker import CeleryTestBroker
from pytest_celery.defaults import ALL_CELERY_BROKERS
from pytest_celery.defaults import CELERY_BROKER_CLUSTER


@pytest.fixture(params=ALL_CELERY_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:  # type: ignore
    broker: CeleryTestBroker = request.getfixturevalue(request.param)
    yield broker
    broker.teardown()


@pytest.fixture
def celery_broker_cluster(celery_broker: CeleryTestBroker) -> CeleryBrokerCluster:  # type: ignore
    cluster = CeleryBrokerCluster(celery_broker)  # type: ignore
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_broker_cluster_config(request: pytest.FixtureRequest) -> dict | None:
    try:
        use_default_config = pytest.fail.Exception
        cluster: CeleryBrokerCluster = request.getfixturevalue(CELERY_BROKER_CLUSTER)
        return cluster.config() if cluster else None
    except use_default_config:
        return CeleryBrokerCluster.default_config()
