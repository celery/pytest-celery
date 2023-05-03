# mypy: disable-error-code="misc"

import pytest

from pytest_celery import defaults
from pytest_celery.api.components.backend import CeleryBackendCluster
from pytest_celery.api.components.backend import CeleryTestBackend


@pytest.fixture(params=defaults.ALL_CELERY_BACKENDS)
def celery_backend(request: pytest.FixtureRequest) -> CeleryTestBackend:  # type: ignore
    backend: CeleryTestBackend = request.getfixturevalue(request.param)
    yield backend
    backend.teardown()


@pytest.fixture
def celery_backend_cluster(celery_backend: CeleryTestBackend) -> CeleryBackendCluster:  # type: ignore
    cluster = CeleryBackendCluster(celery_backend)  # type: ignore
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_backend_cluster_config(request: pytest.FixtureRequest) -> dict:
    try:
        use_default_config = pytest.fail.Exception
        cluster: CeleryBackendCluster = request.getfixturevalue(defaults.CELERY_BACKEND_CLUSTER)
        return cluster.config()
    except use_default_config:
        return CeleryBackendCluster.default_config()
