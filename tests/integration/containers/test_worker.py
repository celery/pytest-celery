import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


@pytest.mark.parametrize("container", lazy_fixture(defaults.ALL_WORKERS_FIXTURES))
class test_celery_worker_container:
    def test_client(self, container: CeleryWorkerContainer):
        assert container.client
        assert container.client == container, "Check tests/conftest.py/WorkerContainer.client"
