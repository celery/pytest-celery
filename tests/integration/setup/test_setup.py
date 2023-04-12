import pytest

from pytest_celery.api.setup import CeleryTestSetup
from tests.common.tasks import identity
from tests.common.test_setup import shared_celery_test_setup_suite


@pytest.fixture
def default_worker_tasks() -> set:
    from tests.common import tasks

    return {tasks}


class test_celery_test_setup(shared_celery_test_setup_suite):
    def test_ready(self, celery_setup: CeleryTestSetup):
        r = identity.s("test_ready").delay()
        assert r.get() == "test_ready"
