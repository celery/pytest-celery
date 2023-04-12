import pytest

from pytest_celery import defaults
from pytest_celery.api.components.worker import CeleryTestWorker
from pytest_celery.api.components.worker import CeleryWorkerCluster


@pytest.fixture(params=defaults.ALL_CELERY_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:
    return request.getfixturevalue(request.param)


@pytest.fixture
def celery_worker_cluster(celery_worker: CeleryTestWorker) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(celery_worker)  # type: ignore


@pytest.fixture
def celery_worker_config(celery_broker_config: dict, celery_backend_config: dict) -> dict:
    return {
        "celery_broker_config": celery_broker_config,
        "celery_backend_config": celery_backend_config,
    }


@pytest.fixture
def celery_worker_cluster_config(celery_broker_cluster_config: dict, celery_backend_cluster_config: dict) -> dict:
    return {
        "celery_broker_cluster_config": celery_broker_cluster_config,
        "celery_backend_cluster_config": celery_backend_cluster_config,
    }
