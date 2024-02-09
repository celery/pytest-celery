"""Every backend component is added to the test matrix using the fixtures of
this module.

These fixtures will configure the test setup for all supported celery
backends by default. Every backend will be executed as a separate test
case, and the test will be executed for each supported celery backend.

You may override these fixtures to customize the test setup for your
specific needs.
"""

# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest

from pytest_celery.api.backend import CeleryBackendCluster
from pytest_celery.api.backend import CeleryTestBackend
from pytest_celery.defaults import ALL_CELERY_BACKENDS
from pytest_celery.defaults import CELERY_BACKEND_CLUSTER


@pytest.fixture(params=ALL_CELERY_BACKENDS)
def celery_backend(request: pytest.FixtureRequest) -> CeleryTestBackend:  # type: ignore
    """Parameterized fixture for all supported celery backends. Responsible for
    tearing down the node.

    This fixture will add parametrization to the test function, so that
    the test will be executed for each supported celery backend.
    """
    backend: CeleryTestBackend = request.getfixturevalue(request.param)
    yield backend
    backend.teardown()


@pytest.fixture
def celery_backend_cluster(celery_backend: CeleryTestBackend) -> CeleryBackendCluster:  # type: ignore
    """Defines the cluster of backend nodes for the test. Responsible for
    tearing down the cluster.

    To disable the cluster, override this fixture and return None.

    Args:
        celery_backend (CeleryTestBackend): Parameterized fixture for all supported celery backends.

    Returns:
        CeleryBackendCluster: Single node cluster for all supported celery backends.
    """
    cluster = CeleryBackendCluster(celery_backend)  # type: ignore
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_backend_cluster_config(request: pytest.FixtureRequest) -> dict | None:
    """Attempts to compile the celery configuration from the cluster."""
    try:
        use_default_config = pytest.fail.Exception
        cluster: CeleryBackendCluster = request.getfixturevalue(CELERY_BACKEND_CLUSTER)
        return cluster.config() if cluster else None
    except use_default_config:
        return CeleryBackendCluster.default_config()
