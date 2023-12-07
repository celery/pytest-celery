from __future__ import annotations

import inspect

import pytest

from pytest_celery import DEFAULT_WORKER_ENV
from pytest_celery import DEFAULT_WORKER_LOG_LEVEL
from pytest_celery import DEFAULT_WORKER_NAME
from pytest_celery import DEFAULT_WORKER_QUEUE
from pytest_celery import DEFAULT_WORKER_VERSION
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryWorkerContainer


class test_celery_worker_container:
    def test_version(self):
        assert CeleryWorkerContainer.version() == DEFAULT_WORKER_VERSION

    def test_log_level(self):
        assert CeleryWorkerContainer.log_level() == DEFAULT_WORKER_LOG_LEVEL

    def test_worker_name(self):
        assert CeleryWorkerContainer.worker_name() == DEFAULT_WORKER_NAME

    def test_worker_queue(self):
        assert CeleryWorkerContainer.worker_queue() == DEFAULT_WORKER_QUEUE

    def test_app_module(self):
        from pytest_celery.vendors.worker import app

        assert CeleryWorkerContainer.app_module() == app

    def test_tasks_modules(self):
        from pytest_celery.vendors.worker import tasks

        assert CeleryWorkerContainer.tasks_modules() == {tasks}

    def test_signals_modules(self):
        assert CeleryWorkerContainer.signals_modules() == set()

    def test_buildargs(self):
        assert CeleryWorkerContainer.buildargs() == {
            "CELERY_VERSION": DEFAULT_WORKER_VERSION,
            "CELERY_LOG_LEVEL": DEFAULT_WORKER_LOG_LEVEL,
            "CELERY_WORKER_NAME": DEFAULT_WORKER_NAME,
            "CELERY_WORKER_QUEUE": DEFAULT_WORKER_QUEUE,
        }

    class test_celery_worker_container_env:
        def test_env(self, celery_worker_cluster_config: dict):
            assert CeleryWorkerContainer.env(celery_worker_cluster_config) == DEFAULT_WORKER_ENV

        class test_disabling_cluster:
            @pytest.fixture
            def celery_backend_cluster(self) -> CeleryBackendCluster:
                return None

            @pytest.fixture
            def celery_broker_cluster(self) -> CeleryBrokerCluster:
                return None

            def test_disabling_clusters(self, celery_worker_cluster_config: dict):
                expected_env = DEFAULT_WORKER_ENV.copy()
                expected_env.pop("CELERY_BROKER_URL")
                expected_env.pop("CELERY_RESULT_BACKEND")
                assert CeleryWorkerContainer.env(celery_worker_cluster_config) == expected_env

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
