from __future__ import annotations

from types import ModuleType

import pytest

from pytest_celery import DEFAULT_WORKER_ENV
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from tests.defaults import ALL_WORKERS_FIXTURES


@pytest.fixture
def container(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("container", ALL_WORKERS_FIXTURES, indirect=["container"])
class test_celery_worker_container:
    def test_client(self, container: CeleryWorkerContainer):
        assert container.client
        assert container.client == container

    def test_celeryconfig(self, container: CeleryWorkerContainer):
        with pytest.raises(NotImplementedError):
            container.celeryconfig

    class test_disabling_cluster:
        @pytest.fixture
        def celery_backend_cluster(self) -> CeleryBackendCluster:
            return None

        def test_disabling_backend_cluster(self, container: CeleryWorkerContainer):
            assert container.logs().count("results:     disabled://")

            results = DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]
            assert container.logs().count(f"transport:   {results}")

    class test_replacing_app_module:
        @pytest.fixture(params=["Default", "Custom"])
        def default_worker_app_module(self, request: pytest.FixtureRequest) -> ModuleType:
            if request.param == "Default":
                return request.getfixturevalue("default_worker_app_module")
            else:
                from pytest_celery.vendors.worker.content import app

                return app

        def test_replacing_app_module(self, container: CeleryWorkerContainer, default_worker_app_module: ModuleType):
            assert container.app_module() == default_worker_app_module


class test_base_test_worker:
    def test_config(self, celery_setup_worker: CeleryTestWorker):
        with pytest.raises(NotImplementedError):
            celery_setup_worker.config()
