# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest

from pytest_celery.api.worker import CeleryTestWorker
from pytest_celery.api.worker import CeleryWorkerCluster
from pytest_celery.defaults import ALL_CELERY_WORKERS


@pytest.fixture(params=ALL_CELERY_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:  # type: ignore
    worker: CeleryTestWorker = request.getfixturevalue(request.param)
    yield worker
    worker.teardown()


@pytest.fixture
def celery_worker_cluster(celery_worker: CeleryTestWorker) -> CeleryWorkerCluster:  # type: ignore
    cluster = CeleryWorkerCluster(celery_worker)  # type: ignore
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_worker_cluster_config(celery_broker_cluster_config: dict, celery_backend_cluster_config: dict) -> dict:
    return {
        "celery_broker_cluster_config": celery_broker_cluster_config,
        "celery_backend_cluster_config": celery_backend_cluster_config,
    }
