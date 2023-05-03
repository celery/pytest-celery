# mypy: disable-error-code="misc"

import pytest

from pytest_celery import defaults
from pytest_celery.api.components.broker import CeleryBrokerCluster
from pytest_celery.api.components.broker import CeleryTestBroker


@pytest.fixture(params=defaults.ALL_CELERY_BROKERS)
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
def celery_broker_cluster_config(request: pytest.FixtureRequest) -> dict:
    try:
        use_default_config = pytest.fail.Exception
        cluster: CeleryBrokerCluster = request.getfixturevalue(defaults.CELERY_BROKER_CLUSTER)
        return cluster.config()
    except use_default_config:
        return CeleryBrokerCluster.default_config()
