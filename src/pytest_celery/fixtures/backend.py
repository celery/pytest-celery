import pytest

from pytest_celery.api.components.backend import CeleryBackendCluster
from pytest_celery.api.components.backend import CeleryTestBackend
from pytest_celery.defaults import FUNCTION_BACKENDS
from pytest_celery.defaults import SESSION_BACKENDS


@pytest.fixture(params=FUNCTION_BACKENDS)
def celery_backend(request: pytest.FixtureRequest) -> CeleryTestBackend:
    return CeleryTestBackend(request.getfixturevalue(request.param))


@pytest.fixture(params=SESSION_BACKENDS)
def celery_session_backend(request: pytest.FixtureRequest) -> CeleryTestBackend:
    return CeleryTestBackend(request.getfixturevalue(request.param))


@pytest.fixture
def celery_backend_cluster(celery_backend: CeleryTestBackend) -> CeleryBackendCluster:
    return CeleryBackendCluster(celery_backend)


@pytest.fixture
def celery_session_backend_cluster(celery_session_backend: CeleryTestBackend) -> CeleryBackendCluster:
    return CeleryBackendCluster(celery_session_backend)
