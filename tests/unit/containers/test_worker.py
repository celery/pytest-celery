import inspect

import pytest

from pytest_celery import CeleryWorkerContainer
from pytest_celery import defaults


class test_celery_worker_container:
    def test_full_ready(self, worker_test_container: CeleryWorkerContainer):
        assert worker_test_container._full_ready(CeleryWorkerContainer.__ready_prompt__)

    def test_client(self, worker_test_container: CeleryWorkerContainer):
        worker_test_container.client

    def test_celeryconfig(self, worker_test_container: CeleryWorkerContainer):
        with pytest.raises(NotImplementedError):
            worker_test_container.celeryconfig

    def test_version(self, worker_test_container: CeleryWorkerContainer):
        assert worker_test_container.version() == defaults.WORKER_CELERY_VERSION

    def test_env(self, worker_test_container: CeleryWorkerContainer, celery_worker_cluster_config: dict):
        assert worker_test_container.env(celery_worker_cluster_config) == defaults.WORKER_ENV

    def test_tasks_modules(self, worker_test_container: CeleryWorkerContainer):
        assert worker_test_container.tasks_modules() == set()

    def test_initial_content_default_tasks(self, worker_test_container: CeleryWorkerContainer):
        from tests.common import tasks

        expected_partial_initial_content = {
            "__init__.py": b"",
            "tests/common/tasks.py": inspect.getsource(tasks).encode(),
        }
        actual_initial_content = worker_test_container.initial_content({tasks})
        assert "app.py" in actual_initial_content
        for key, value in expected_partial_initial_content.items():
            assert actual_initial_content[key] == value

    def test_initial_content_import_formatting(self, worker_test_container: CeleryWorkerContainer):
        from tests.common import tasks

        actual_initial_content = worker_test_container.initial_content({tasks})
        assert "from tests.common.tasks import *" in str(actual_initial_content["app.py"])

    def test_task_modules(self, worker_test_container: CeleryWorkerContainer):
        assert worker_test_container.tasks_modules() == set()
