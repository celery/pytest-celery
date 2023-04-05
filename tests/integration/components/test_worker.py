import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker


@pytest.mark.parametrize("node", [lazy_fixture(defaults.CELERY_TEST_WORKER)])
class test_base_test_worker:
    def test_ready(self, node: CeleryTestWorker):
        assert node.ready()
