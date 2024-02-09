"""The :ref:`built-in-worker` is added to the test matrix using the fixtures of
this module.

These fixtures will configure the test setup for the built-in Celery
worker by default.

You may override these fixtures to customize the test setup for your
specific needs.
"""

# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest

from pytest_celery.api.worker import CeleryTestWorker
from pytest_celery.api.worker import CeleryWorkerCluster
from pytest_celery.defaults import ALL_CELERY_WORKERS


@pytest.fixture(params=ALL_CELERY_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:  # type: ignore
    """Parameterized fixture for all supported celery workers. Responsible for
    tearing down the node.

    This fixture will add parametrization to the test function, so that
    the test will be executed for each supported celery worker.
    """

    worker: CeleryTestWorker = request.getfixturevalue(request.param)
    yield worker
    worker.teardown()


@pytest.fixture
def celery_worker_cluster(celery_worker: CeleryTestWorker) -> CeleryWorkerCluster:  # type: ignore
    """Defines the cluster of worker nodes for the test. Responsible for
    tearing down the cluster.

    To disable the cluster, override this fixture and return None.

    Args:
        celery_worker (CeleryTestWorker): Parameterized fixture for all supported celery workers.

    Returns:
        CeleryWorkerCluster: Single node cluster for all supported celery workers.
    """
    cluster = CeleryWorkerCluster(celery_worker)  # type: ignore
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_worker_cluster_config(celery_broker_cluster_config: dict, celery_backend_cluster_config: dict) -> dict:
    """Combine the broker and backend cluster configurations.

    Additional configuration can be added.
    """
    return {
        "celery_broker_cluster_config": celery_broker_cluster_config,
        "celery_backend_cluster_config": celery_backend_cluster_config,
    }
