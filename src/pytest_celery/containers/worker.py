import inspect

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class CeleryWorkerContainer(CeleryTestContainer):
    def ready(self) -> bool:
        return self._full_ready("ready.")

    @classmethod
    def version(cls) -> str:
        return defaults.FUNCTION_WORKER_VERSION

    @classmethod
    def env(cls, celery_worker_config: dict) -> dict:
        celery_broker_config = celery_worker_config["celery_broker_config"]
        celery_backend_config = celery_worker_config["celery_backend_config"]
        celery_worker_config = {
            "CELERY_BROKER_URL": celery_broker_config["url"],
            "CELERY_RESULT_BACKEND": celery_backend_config["url"],
        }
        return {**defaults.FUNCTION_WORKER_ENV, **celery_worker_config}

    @classmethod
    def initial_content(cls, function_worker_tasks: set) -> dict:
        from pytest_celery.components.worker import app as app_module
        from pytest_celery.components.worker import common

        function_worker_tasks.add(common)

        app_module_src = inspect.getsource(app_module)
        import_string = ""

        for module in function_worker_tasks:
            import_string += f"from {module.__name__} import *\n"

        app_module_src = app_module_src.format(import_string)

        initial_content = {
            "__init__.py": b"",
            "app.py": app_module_src.encode(),
        }
        if function_worker_tasks:
            function_worker_tasks_src = {
                f"{module.__name__.replace('.', '/')}.py": inspect.getsource(module).encode()
                for module in function_worker_tasks
            }
            initial_content.update(function_worker_tasks_src)
        else:
            print("No tasks found")
        return initial_content

    @classmethod
    def tasks_modules(cls) -> set:
        return set()
