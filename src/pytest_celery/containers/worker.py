import inspect

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class CeleryWorkerContainer(CeleryTestContainer):
    __ready_prompt__ = "ready."

    def ready(self) -> bool:
        return self._full_ready(self.__ready_prompt__)

    @classmethod
    def version(cls) -> str:
        return defaults.DEFAULT_WORKER_VERSION

    @classmethod
    def env(cls, celery_worker_cluster_config: dict) -> dict:
        celery_broker_cluster_config = celery_worker_cluster_config.get("celery_broker_cluster_config")
        celery_backend_cluster_config = celery_worker_cluster_config.get("celery_backend_cluster_config")
        env = {}
        if celery_broker_cluster_config:
            env["CELERY_BROKER_URL"] = ";".join(celery_broker_cluster_config["urls"])
        if celery_backend_cluster_config:
            env["CELERY_RESULT_BACKEND"] = ";".join(celery_backend_cluster_config["urls"])
        return {**defaults.DEFAULT_WORKER_ENV, **env}

    @classmethod
    def initial_content(cls, default_worker_tasks: set) -> dict:
        from pytest_celery.components.worker import app as app_module
        from pytest_celery.components.worker import common

        default_worker_tasks.add(common)

        app_module_src = inspect.getsource(app_module)
        import_string = ""

        for module in default_worker_tasks:
            import_string += f"from {module.__name__} import *\n"

        app_module_src = app_module_src.format(import_string)

        initial_content = {
            "__init__.py": b"",
            "app.py": app_module_src.encode(),
        }
        if default_worker_tasks:
            default_worker_tasks_src = {
                f"{module.__name__.replace('.', '/')}.py": inspect.getsource(module).encode()
                for module in default_worker_tasks
            }
            initial_content.update(default_worker_tasks_src)
        else:
            print("No tasks found")
        return initial_content

    @classmethod
    def tasks_modules(cls) -> set:
        return set()
