import pytest

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from tests.common.celery4.fixtures import *  # noqa

C5_C4_WORKERS = defaults.ALL_CELERY_WORKERS + ("celery4_test_worker",)


@pytest.fixture(params=C5_C4_WORKERS)
def celery_worker(request: pytest.FixtureRequest) -> CeleryTestWorker:
    return request.getfixturevalue(request.param)


@pytest.fixture
def function_worker_tasks() -> set:
    from tests.common import tasks as common_tasks
    from tests.smoke import tasks as smoke_tasks

    return {
        common_tasks,
        smoke_tasks,
    }
