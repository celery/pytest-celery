import inspect
from typing import Union

from celery import Celery
from celery.app.base import PendingConfiguration

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_ENV
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_LOG_LEVEL
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_NAME
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_QUEUE
from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_VERSION


class CeleryWorkerContainer(CeleryTestContainer):
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
    def buildargs(cls) -> dict:
        return {
            "CELERY_VERSION": cls.version(),
            "CELERY_LOG_LEVEL": cls.log_level(),
            "CELERY_WORKER_NAME": cls.worker_name(),
            "CELERY_WORKER_QUEUE": cls.worker_queue(),
        }

    @classmethod
    def env(cls, celery_worker_cluster_config: dict) -> dict:
        celery_broker_cluster_config = celery_worker_cluster_config.get("celery_broker_cluster_config")
        celery_backend_cluster_config = celery_worker_cluster_config.get("celery_backend_cluster_config")
        env = {}
        if celery_broker_cluster_config:
            env["CELERY_BROKER_URL"] = ";".join(celery_broker_cluster_config["urls"])
        if celery_backend_cluster_config:
            env["CELERY_RESULT_BACKEND"] = ";".join(celery_backend_cluster_config["urls"])
        return {**DEFAULT_WORKER_ENV, **env}

    @classmethod
    def initial_content(
        cls,
        worker_tasks: set,
        worker_signals: Union[set, None] = None,
        worker_app: Union[Celery, None] = None,
    ) -> dict:
        from pytest_celery.vendors.worker import app as app_module

        app_module_src = inspect.getsource(app_module)

        imports = dict()
        initial_content = cls._initial_content_worker_tasks(worker_tasks)
        imports["tasks_imports"] = initial_content.pop("tasks_imports")
        if worker_signals:
            initial_content.update(cls._initial_content_worker_signals(worker_signals))
            imports["signals_imports"] = initial_content.pop("signals_imports")
        if worker_app:
            # Accessing the worker_app.conf.changes.data property will trigger the PendingConfiguration to be resolved
            # and the changes will be applied to the worker_app.conf, so we make a clone app to avoid affecting the
            # original app object.
            app = Celery(worker_app.main)
            app.conf = worker_app.conf
            config_changes_from_defaults = app.conf.changes.copy()
            if isinstance(config_changes_from_defaults, PendingConfiguration):
                config_changes_from_defaults = config_changes_from_defaults.data.changes
            if not isinstance(config_changes_from_defaults, dict):
                raise TypeError(f"Unexpected type for config_changes: {type(config_changes_from_defaults)}")
            del config_changes_from_defaults["deprecated_settings"]

            name_code = f'name = "{worker_app.main}"'
        else:
            config_changes_from_defaults = {}
            name_code = f'name = "{cls.worker_name()}"'

        imports_format = "{%s}" % "}{".join(imports.keys())
        imports_format = imports_format.format(**imports)
        app_module_src = app_module_src.replace("{0}", imports_format)

        app_module_src = app_module_src.replace("{1}", name_code)

        config_items = (f"    {repr(key)}: {repr(value)}" for key, value in config_changes_from_defaults.items())
        config_code = (
            "config_updates = {\n" + ",\n".join(config_items) + "\n}"
            if config_changes_from_defaults
            else "config_updates = {}"
        )
        app_module_src = app_module_src.replace("{2}", config_code)

        initial_content["app.py"] = app_module_src.encode()
        return initial_content

    @classmethod
    def _initial_content_worker_tasks(cls, worker_tasks: set) -> dict:
        from pytest_celery.vendors.worker import tasks

        worker_tasks.add(tasks)

        import_string = ""

        for module in worker_tasks:
            import_string += f"from {module.__name__} import *\n"

        initial_content = {
            "__init__.py": b"",
            "tasks_imports": import_string,
        }
        if worker_tasks:
            default_worker_tasks_src = {
                f"{module.__name__.replace('.', '/')}.py": inspect.getsource(module).encode() for module in worker_tasks
            }
            initial_content.update(default_worker_tasks_src)
        else:
            print("No tasks found")
        return initial_content

    @classmethod
    def _initial_content_worker_signals(cls, worker_signals: set) -> dict:
        import_string = ""

        for module in worker_signals:
            import_string += f"from {module.__name__} import *\n"

        initial_content = {
            "__init__.py": b"",
            "signals_imports": import_string,
        }
        if worker_signals:
            default_worker_signals_src = {
                f"{module.__name__.replace('.', '/')}.py": inspect.getsource(module).encode()
                for module in worker_signals
            }
            initial_content.update(default_worker_signals_src)
        else:
            print("No signals found")
        return initial_content

    @classmethod
    def tasks_modules(cls) -> set:
        return set()

    @classmethod
    def signals_modules(cls) -> set:
        return set()

    def _wait_port(self, port: str) -> int:
        raise NotImplementedError

    @property
    def ready_prompt(self) -> str:
        return "ready."
