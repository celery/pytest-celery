import pytest

from pytest_celery.api.components.broker import CeleryBrokerCluster
from pytest_celery.api.components.broker import CeleryTestBroker
from pytest_celery.defaults import FUNCTION_BROKERS
from pytest_celery.defaults import SESSION_BROKERS


@pytest.fixture(params=SESSION_BROKERS)
def celery_session_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:
    return CeleryTestBroker(request.getfixturevalue(request.param))


@pytest.fixture(params=FUNCTION_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:
    return CeleryTestBroker(request.getfixturevalue(request.param))


@pytest.fixture
def celery_session_broker_cluster(celery_session_broker: CeleryTestBroker) -> CeleryBrokerCluster:
    return CeleryBrokerCluster(celery_session_broker)


@pytest.fixture
def celery_broker_cluster(celery_broker: CeleryTestBroker) -> CeleryBrokerCluster:
    return CeleryBrokerCluster(celery_broker)
