import pytest

from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.setup import CeleryTestSetup


@pytest.fixture
def celery_setup(
    celery_session_backend_cluster: CeleryBackendCluster, celery_session_broker_cluster: CeleryBrokerCluster
) -> CeleryTestSetup:
    setup = CeleryTestSetup(
        backend_cluster=celery_session_backend_cluster, broker_cluster=celery_session_broker_cluster
    )
    while not setup.ready():
        pass
    return setup
