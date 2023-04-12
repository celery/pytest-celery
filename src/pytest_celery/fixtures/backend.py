import pytest

from pytest_celery import defaults
from pytest_celery.api.components.backend import CeleryBackendCluster
from pytest_celery.api.components.backend import CeleryTestBackend


@pytest.fixture(params=defaults.ALL_CELERY_BACKENDS)
def celery_backend(request: pytest.FixtureRequest) -> CeleryTestBackend:
    return request.getfixturevalue(request.param)


@pytest.fixture
def celery_backend_cluster(celery_backend: CeleryTestBackend) -> CeleryBackendCluster:
    return CeleryBackendCluster(celery_backend)  # type: ignore


@pytest.fixture
def celery_backend_config(request: pytest.FixtureRequest) -> dict:
    try:
        celery_backend: CeleryTestBackend = request.getfixturevalue(defaults.CELERY_BACKEND)
        return celery_backend.config()
    except BaseException:
        # TODO: Add logging
        return CeleryTestBackend.default_config()


@pytest.fixture
def celery_backend_cluster_config(request: pytest.FixtureRequest) -> dict:
    try:
        celery_backend_cluster: CeleryBackendCluster = request.getfixturevalue(defaults.CELERY_BACKEND_CLUSTER)
        return celery_backend_cluster.config()
    except BaseException:
        # TODO: Add logging
        return CeleryBackendCluster.default_config()
