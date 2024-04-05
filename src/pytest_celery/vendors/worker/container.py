"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the :ref:`built-in-worker` vendor.
"""

from __future__ import annotations

from types import ModuleType

from celery import Celery

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_ENV
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_LOG_LEVEL
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_NAME
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_PORTS
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_QUEUE
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_VERSION
from pytest_celery.vendors.worker.volume import WorkerInitialContent


class CeleryWorkerContainer(CeleryTestContainer):
    """This is the base class for all Celery worker containers. It is
    preconfigured for a built-in Celery worker image and should be customized
    for your own worker image.

    The purpose of this class is manipulating the container volume and
    configurations to warm up the worker container according to the test case requirements.

    Responsibility Scope:
        Prepare the worker container with the required filesystem, configurations and
        dependencies of your project.
    """

    @classmethod
    def command(
        cls,
        *args: str,
        debugpy: bool = False,
        wait_for_client: bool = True,
        **kwargs: dict,
    ) -> list[str]:
        args = args or tuple()
        cmd = list()

        if debugpy:
            cmd.extend(
                [
                    "python",
                    "-m",
                    "debugpy",
                    "--listen",
                    "0.0.0.0:5678",
                ]
            )

            if wait_for_client:
                cmd.append("--wait-for-client")

            cmd.append("-m")

        cmd.extend(
            [
                "celery",
                "-A",
                "app",
                "worker",
                f"--loglevel={cls.log_level()}",
                "-n",
                f"{cls.worker_name()}@%h",
                "-Q",
                f"{cls.worker_queue()}",
                *args,
            ]
        )

        return cmd

    def _wait_port(self, port: str) -> int:
        # Not needed for worker container
        raise NotImplementedError

    @property
    def ready_prompt(self) -> str:
        return "ready."

    @classmethod
    def version(cls) -> str:
        """Celery version to use for the worker container."""
        return DEFAULT_WORKER_VERSION

    @classmethod
    def log_level(cls) -> str:
        """Celery worker log level."""
        return DEFAULT_WORKER_LOG_LEVEL

    @classmethod
    def worker_name(cls) -> str:
        """Celery worker name."""
        return DEFAULT_WORKER_NAME

    @classmethod
    def worker_queue(cls) -> str:
        """Celery worker queue."""
        return DEFAULT_WORKER_QUEUE

    @classmethod
    def app_module(cls) -> ModuleType:
        """A preconfigured module that contains the Celery app instance.

        The module is manipulated at runtime to inject the required
        configurations from the test case.
        """
        from pytest_celery.vendors.worker.content import app

        return app

    @classmethod
    def utils_module(cls) -> ModuleType:
        """A utility helper module for running python code in the worker
        container context."""
        from pytest_celery.vendors.worker.content import utils

        return utils

    @classmethod
    def tasks_modules(cls) -> set:
        """Tasks modules."""
        from pytest_celery.vendors.worker import tasks as default_tasks

        return {default_tasks}

    @classmethod
    def signals_modules(cls) -> set:
        """Signals handlers modules.

        This is an optional feature that can be used to inject signals
        handlers that needs to in the context of the worker container.
        """
        return set()

    @classmethod
    def buildargs(cls) -> dict:
        """Build arguments for the built-in worker image."""
        return {
            "CELERY_VERSION": cls.version(),
            "CELERY_LOG_LEVEL": cls.log_level(),
            "CELERY_WORKER_NAME": cls.worker_name(),
            "CELERY_WORKER_QUEUE": cls.worker_queue(),
        }

    @classmethod
    def initial_env(cls, celery_worker_cluster_config: dict, initial: dict | None = None) -> dict:
        """Defines the environment variables for the worker container.

        See more: pytest_docker_tools.container()

        Args:
            celery_worker_cluster_config (dict): Environment variables to set.
            initial (dict | None, optional): Additional variables. Defaults to None.

        Returns:
            dict: Environment variables set for the worker container from the test case.
        """
        env = initial or {}
        env = {
            **DEFAULT_WORKER_ENV.copy(),
            **env,
        }

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
        utils_module: ModuleType | None = None,
    ) -> dict:
        """Defines the initial content of the worker container.

        See more: pytest_docker_tools.volume()

        Args:
            worker_tasks (set | None, optional): Set of tasks modules. Defaults to None.
            worker_signals (set | None, optional): Set of signals handlers modules. Defaults to None.
            worker_app (Celery | None, optional): Celery app instance. Defaults to None.
            app_module (ModuleType | None, optional): app module. Defaults to None.
            utils_module (ModuleType | None, optional): utils module. Defaults to None.

        Returns:
            dict: Custom volume content for the worker container.
        """
        if app_module is None:
            app_module = cls.app_module()

        if utils_module is None:
            utils_module = cls.utils_module()

        if worker_tasks is None:
            worker_tasks = cls.tasks_modules()

        content = WorkerInitialContent()
        content.set_app_module(app_module)
        content.set_utils_module(utils_module)
        content.add_modules("tasks", worker_tasks)
        if worker_signals:
            content.add_modules("signals", worker_signals)
        if worker_app:
            content.set_app_name(worker_app.main)
            content.set_config_from_object(worker_app)

        return content.generate()

    @classmethod
    def ports(cls) -> dict | None:
        """Ports to expose from the worker container."""
        return DEFAULT_WORKER_PORTS
