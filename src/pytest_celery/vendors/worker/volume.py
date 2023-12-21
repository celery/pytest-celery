from __future__ import annotations

import inspect
from types import ModuleType
from typing import Any

from celery import Celery
from celery.app.base import PendingConfiguration

from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_APP_NAME


class WorkerInitialContent:
    class Parser:
        def imports_str(self, modules: set[ModuleType]) -> str:
            return "".join(f"from {module.__name__} import *\n" for module in modules)

        def imports_src(self, modules: set[ModuleType]) -> dict:
            src = dict()
            for module in modules:
                src[f"{module.__name__.replace('.', '/')}.py"] = inspect.getsource(module).encode()
            return src

        def app_name(self, name: str | None = None) -> str:
            name = name or DEFAULT_WORKER_APP_NAME
            return f"app = Celery('{name}')"

        def config(self, app: Celery | None = None) -> str:
            app = app or Celery(DEFAULT_WORKER_APP_NAME)

            # Accessing the app.conf.changes.data property will trigger the PendingConfiguration to be resolved
            # and the changes will be applied to the app.conf, so we make a clone app to avoid affecting the
            # original app object.
            tmp_app = Celery(app.main)
            tmp_app.conf = app.conf

            changes = tmp_app.conf.changes.copy()
            if isinstance(changes, PendingConfiguration):
                changes = changes.data.changes
            if not isinstance(changes, dict):
                raise TypeError(f"Unexpected type for app.conf.changes: {type(changes)}")
            del changes["deprecated_settings"]

            if changes:
                changes = (f"\t{repr(key)}: {repr(value)}" for key, value in changes.items())
                config = "config = {\n" + ",\n".join(changes) + "\n}" if changes else "config = None"
            else:
                config = "config = None"
            return config

    def __init__(
        self,
        app_module: ModuleType | None = None,
        utils_module: ModuleType | None = None,
    ) -> None:
        self.parser = self.Parser()
        self._initial_content = {
            "__init__.py": b"",
            "imports": dict(),  # Placeholder item
        }
        self.set_app_module(app_module)
        self.set_utils_module(utils_module)
        self.set_app_name()
        self.set_config_from_object()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, WorkerInitialContent):
            return False
        try:
            return self.generate() == __value.generate()
        except ValueError:
            return all(
                [
                    self._app_module_src == __value._app_module_src,
                    self._utils_module_src == __value._utils_module_src,
                    self._initial_content == __value._initial_content,
                    self._app == __value._app,
                    self._config == __value._config,
                ]
            )

    def set_app_module(self, app_module: ModuleType | None = None) -> None:
        self._app_module_src: str | None

        if app_module:
            self._app_module_src = inspect.getsource(app_module)
        else:
            self._app_module_src = None

    def set_utils_module(self, utils_module: ModuleType | None = None) -> None:
        self._utils_module_src: str | None

        if utils_module:
            self._utils_module_src = inspect.getsource(utils_module)
        else:
            self._utils_module_src = None

    def add_modules(self, name: str, modules: set[ModuleType]) -> None:
        if not name:
            raise ValueError("name cannot be empty")

        if not modules:
            raise ValueError("modules cannot be empty")

        self._initial_content["imports"][name] = self.parser.imports_str(modules)  # type: ignore
        self._initial_content.update(self.parser.imports_src(modules))

    def set_app_name(self, name: str | None = None) -> None:
        name = name or DEFAULT_WORKER_APP_NAME
        self._app = self.parser.app_name(name)

    def set_config_from_object(self, app: Celery | None = None) -> None:
        self._config = self.parser.config(app)

    def generate(self) -> dict:
        initial_content = self._initial_content.copy()
        initial_content["app.py"] = self._generate_app_py(initial_content)
        initial_content["utils.py"] = self._generate_utils_py()
        return initial_content

    def _generate_app_py(self, initial_content: dict) -> bytes:
        if not self._app_module_src:
            raise ValueError("Please set_app_module() before generating initial content")

        if not initial_content["imports"]:
            raise ValueError("Please add_modules() before generating initial content")

        _imports: dict | Any = initial_content.pop("imports")
        imports = "{%s}" % "}{".join(_imports.keys())
        imports = imports.format(**_imports)

        app, config = self._app, self._config

        replacement_args = {
            "imports": "imports = None",
            "app": f'app = Celery("{DEFAULT_WORKER_APP_NAME}")',
            "config": "config = None",
        }
        self._app_module_src = self._app_module_src.replace(replacement_args["imports"], imports)
        self._app_module_src = self._app_module_src.replace(replacement_args["app"], app)
        self._app_module_src = self._app_module_src.replace(replacement_args["config"], config)

        return self._app_module_src.encode()

    def _generate_utils_py(self) -> bytes:
        if not self._utils_module_src:
            raise ValueError("Please set_utils_module() before generating initial content")

        return self._utils_module_src.encode()
