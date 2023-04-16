from typing import Type

import pytest

from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.api.setup import CeleryTestSetup
from tests.common.celery4.api import Worker4Container
from tests.common.celery4.fixtures import *  # noqa
from tests.common.tasks import identity
from tests.common.test_setup import shared_celery_test_setup_suite


class Celery5TestWorker(CeleryTestWorker):
    @property
    def version(self) -> str:
        return "5.2.7"


@pytest.fixture
def default_worker_cls() -> Type[CeleryTestWorker]:
    # TODO: Make/add class decorator
    return Celery5TestWorker


@pytest.fixture(scope="session")
def default_worker_celery_version() -> str:
    return "5.2.7"


@pytest.fixture
def default_worker_tasks() -> set:
    from tests.common import tasks

    return {tasks}


@pytest.fixture
def celery_worker_cluster(
    celery_worker: CeleryTestWorker,
    celery4_worker: CeleryTestWorker,
) -> CeleryWorkerCluster:
    return CeleryWorkerCluster(
        celery_worker,
        celery4_worker,
    )


class test_custom_setup(shared_celery_test_setup_suite):
    def test_celery_setup_override(self, celery_setup: CeleryTestSetup):
        # TODO: Set each task to use a different queue/worker respectively
        r1 = identity.s("test_ready").delay()
        r2 = identity.s("test_ready").delay()
        assert r1.get(timeout=60) == "test_ready"
        assert r2.get(timeout=60) == "test_ready"
        assert celery_setup.app

    def test_custom_cluster_version(self, celery_setup: CeleryTestSetup, default_worker_celery_version: str):
        assert len(celery_setup.worker_cluster) == 2
        assert celery_setup.worker_cluster.versions == {
            default_worker_celery_version,
            Worker4Container.version(),
        }
