import inspect

from celery import Celery

from pytest_celery import DEFAULT_WORKER_ENV
from pytest_celery import DEFAULT_WORKER_VERSION
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer


class test_celery_worker_container:
    def test_version(self):
        assert CeleryWorkerContainer.version() == DEFAULT_WORKER_VERSION

    def test_env(self, celery_worker_cluster_config: dict):
        assert CeleryWorkerContainer.env(celery_worker_cluster_config) == DEFAULT_WORKER_ENV

    def test_tasks_modules(self):
        assert CeleryWorkerContainer.tasks_modules() == set()

    def test_initial_content_default_tasks(self):
        from tests import tasks

        expected_partial_initial_content = {
            "__init__.py": b"",
            "tests/tasks.py": inspect.getsource(tasks).encode(),
        }
        actual_initial_content = CeleryWorkerContainer.initial_content({tasks})
        assert "app.py" in actual_initial_content
        for key, value in expected_partial_initial_content.items():
            assert actual_initial_content[key] == value

    def test_initial_content_import_formatting(self):
        from tests import tasks

        actual_initial_content = CeleryWorkerContainer.initial_content({tasks})
        assert "from tests.tasks import *" in str(actual_initial_content["app.py"])

    def test_task_modules(self):
        assert CeleryWorkerContainer.tasks_modules() == set()


class test_base_worker_api:
    def test_ready(self, celery_setup_worker: CeleryTestWorker):
        celery_setup_worker.ready()
        celery_setup_worker.container.ready.assert_called_once()

    def test_app(self, celery_setup_worker: CeleryTestWorker, celery_setup_app: Celery):
        assert celery_setup_worker.app is celery_setup_app

    def test_version(self, celery_setup_worker: CeleryTestWorker):
        assert celery_setup_worker.version == CeleryWorkerContainer.version()
