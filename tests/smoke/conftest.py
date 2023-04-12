import pytest

from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from tests.common.celery4.fixtures import *  # noqa


@pytest.fixture(
    # Each param item is a list of workers to be used in the cluster
    params=[
        ["celery_test_worker"],
        ["celery4_test_worker"],
        ["celery_test_worker", "celery4_test_worker"],
    ]
)
def celery_worker_cluster(request: pytest.FixtureRequest) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(*[request.getfixturevalue(worker) for worker in request.param])


@pytest.fixture
def default_worker_tasks() -> set:
    from tests.common import tasks as common_tasks
    from tests.smoke import tasks as smoke_tasks

    return {
        common_tasks,
        smoke_tasks,
    }
