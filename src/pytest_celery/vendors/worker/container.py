from __future__ import annotations

from types import ModuleType

from celery import Celery

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_ENV
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_LOG_LEVEL
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_NAME
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_QUEUE
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_VERSION
from pytest_celery.vendors.worker.volume import WorkerInitialContent


class CeleryWorkerContainer(CeleryTestContainer):
    def _wait_port(self, port: str) -> int:
        raise NotImplementedError

    @property
    def ready_prompt(self) -> str:
        return "ready."

    @classmethod
    def version(cls) -> str:
        return DEFAULT_WORKER_VERSION

    @classmethod
    def log_level(cls) -> str:
        return DEFAULT_WORKER_LOG_LEVEL

    @classmethod
    def worker_name(cls) -> str:
        return DEFAULT_WORKER_NAME

    @classmethod
    def worker_queue(cls) -> str:
        return DEFAULT_WORKER_QUEUE

    @classmethod
    def app_module(cls) -> ModuleType:
        from pytest_celery.vendors.worker.content import app

        return app

    @classmethod
    def tasks_modules(cls) -> set:
        from pytest_celery.vendors.worker import tasks

        return {tasks}

    @classmethod
    def signals_modules(cls) -> set:
        return set()

    @classmethod
    def buildargs(cls) -> dict:
        return {
            "CELERY_VERSION": cls.version(),
            "CELERY_LOG_LEVEL": cls.log_level(),
            "CELERY_WORKER_NAME": cls.worker_name(),
            "CELERY_WORKER_QUEUE": cls.worker_queue(),
        }

    @classmethod
    def env(cls, celery_worker_cluster_config: dict, initial: dict | None = None) -> dict:
        env = initial or {}
        env = {**env, **DEFAULT_WORKER_ENV.copy()}

        config_mappings = [
            ("celery_broker_cluster_config", "CELERY_BROKER_URL"),
            ("celery_backend_cluster_config", "CELERY_RESULT_BACKEND"),
        ]

        for config_key, env_key in config_mappings:
            cluster_config = celery_worker_cluster_config.get(config_key)
            if cluster_config:
                env[env_key] = ";".join(cluster_config["urls"])
            else:
                del env[env_key]

        return env

    @classmethod
    def initial_content(
        cls,
        worker_tasks: set | None = None,
        worker_signals: set | None = None,
        worker_app: Celery | None = None,
        app_module: ModuleType | None = None,
    ) -> dict:
        if app_module is None:
            app_module = cls.app_module()

        if worker_tasks is None:
            worker_tasks = cls.tasks_modules()

        content = WorkerInitialContent()
        content.set_app_module(app_module)
        content.add_modules("tasks", worker_tasks)
        if worker_signals:
            content.add_modules("signals", worker_signals)
        if worker_app:
            content.set_app_name(worker_app.main)
            content.set_config_from_object(worker_app)

        return content.generate()
