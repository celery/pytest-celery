import pytest

from pytest_celery import defaults
from pytest_celery.api.components.broker import CeleryBrokerCluster
from pytest_celery.api.components.broker import CeleryTestBroker


@pytest.fixture(params=defaults.ALL_CELERY_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:
    return request.getfixturevalue(request.param)


@pytest.fixture
def celery_broker_cluster(celery_broker: CeleryTestBroker) -> CeleryBrokerCluster:
    return CeleryBrokerCluster(celery_broker)  # type: ignore


@pytest.fixture
def celery_broker_config(request: pytest.FixtureRequest) -> dict:
    try:
        celery_broker: CeleryTestBroker = request.getfixturevalue(defaults.CELERY_BROKER)
        return celery_broker.container.celeryconfig()
    except BaseException:
        return {
            "url": defaults.WORKER_ENV["CELERY_BROKER_URL"],
            "local_url": defaults.WORKER_ENV["CELERY_BROKER_URL"],
        }
