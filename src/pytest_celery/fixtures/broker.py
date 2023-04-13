import pytest

from pytest_celery import defaults
from pytest_celery.api.components.broker import CeleryBrokerCluster
from pytest_celery.api.components.broker import CeleryTestBroker
from pytest_celery.utils import resilient_getfixturevalue


@pytest.fixture(params=defaults.ALL_CELERY_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:
    return resilient_getfixturevalue(request)


@pytest.fixture
def celery_broker_cluster(celery_broker: CeleryTestBroker) -> CeleryBrokerCluster:
    return CeleryBrokerCluster(celery_broker)  # type: ignore


@pytest.fixture
def celery_broker_config(request: pytest.FixtureRequest) -> dict:
    try:
        celery_broker: CeleryTestBroker = request.getfixturevalue(defaults.CELERY_BROKER)
        return celery_broker.config()
    except BaseException:
        # TODO: Add logging
        return CeleryTestBroker.default_config()


@pytest.fixture
def celery_broker_cluster_config(
    request: pytest.FixtureRequest,
) -> dict:
    try:
        celery_broker_cluster: CeleryBrokerCluster = request.getfixturevalue(defaults.CELERY_BROKER_CLUSTER)
        return celery_broker_cluster.config()
    except BaseException:
        # TODO: Add logging
        return CeleryBrokerCluster.default_config()
