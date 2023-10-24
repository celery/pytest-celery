import pytest
from pytest_lazyfixture import lazy_fixture

# from pytest_celery import CELERY_SETUP_WORKER
# from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from tests.defaults import ALL_WORKERS_FIXTURES


@pytest.mark.parametrize("container", lazy_fixture(ALL_WORKERS_FIXTURES))
class test_celery_worker_container:
    def test_client(self, container: CeleryWorkerContainer):
        assert container.client
        assert container.client == container

    def test_celeryconfig(self, container: CeleryWorkerContainer):
        with pytest.raises(NotImplementedError):
            container.celeryconfig


# @pytest.mark.parametrize("node", [lazy_fixture(CELERY_SETUP_WORKER)])
# class test_base_test_worker:
#     def test_placeholder(self, node: CeleryTestWorker):
#         node = node
