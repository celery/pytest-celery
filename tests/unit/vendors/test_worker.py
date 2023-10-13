import inspect

import pytest
from celery import Celery

from pytest_celery import WORKER_CELERY_VERSION
from pytest_celery import WORKER_ENV
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from tests.unit.docker.api import UnitWorkerContainer


class test_celery_worker_container:
    def test_client(self, worker_test_container: CeleryWorkerContainer):
        worker_test_container.client

    def test_celeryconfig(self, worker_test_container: CeleryWorkerContainer):
        with pytest.raises(NotImplementedError):
            worker_test_container.celeryconfig

    def test_version(self, worker_test_container: CeleryWorkerContainer):
        assert worker_test_container.version() == WORKER_CELERY_VERSION

    def test_env(self, worker_test_container: CeleryWorkerContainer, celery_worker_cluster_config: dict):
        assert worker_test_container.env(celery_worker_cluster_config) == WORKER_ENV

    def test_tasks_modules(self, worker_test_container: CeleryWorkerContainer):
        assert worker_test_container.tasks_modules() == set()

    def test_initial_content_default_tasks(self, worker_test_container: CeleryWorkerContainer):
        from tests import tasks

        expected_partial_initial_content = {
            "__init__.py": b"",
            "tests/tasks.py": inspect.getsource(tasks).encode(),
        }
        actual_initial_content = worker_test_container.initial_content({tasks})
        assert "app.py" in actual_initial_content
        for key, value in expected_partial_initial_content.items():
            assert actual_initial_content[key] == value

    def test_initial_content_import_formatting(self, worker_test_container: CeleryWorkerContainer):
        from tests import tasks

        actual_initial_content = worker_test_container.initial_content({tasks})
        assert "from tests.tasks import *" in str(actual_initial_content["app.py"])

    def test_task_modules(self, worker_test_container: CeleryWorkerContainer):
        assert worker_test_container.tasks_modules() == set()


class test_base_test_worker:
    def test_ready(self, celery_setup_worker: CeleryTestWorker):
        assert celery_setup_worker.ready()

    def test_app(self, celery_setup_worker: CeleryTestWorker, celery_setup_app: Celery):
        assert celery_setup_worker.app is celery_setup_app

    def test_wait_for_log(self, celery_setup_worker: CeleryTestWorker):
        log = f"{UnitWorkerContainer.worker_name()}@{celery_setup_worker.hostname()} v{celery_setup_worker.version}"
        celery_setup_worker.wait_for_log(log, "test_base_test_worker.test_wait_for_log")
