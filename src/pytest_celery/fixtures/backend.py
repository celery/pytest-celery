# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest

from pytest_celery.api.backend import CeleryBackendCluster
from pytest_celery.api.backend import CeleryTestBackend
from pytest_celery.defaults import ALL_CELERY_BACKENDS
from pytest_celery.defaults import CELERY_BACKEND_CLUSTER


@pytest.fixture(params=ALL_CELERY_BACKENDS)
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
def celery_backend_cluster_config(request: pytest.FixtureRequest) -> dict | None:
    try:
        use_default_config = pytest.fail.Exception
        cluster: CeleryBackendCluster = request.getfixturevalue(CELERY_BACKEND_CLUSTER)
        return cluster.config() if cluster else None
    except use_default_config:
        return CeleryBackendCluster.default_config()
