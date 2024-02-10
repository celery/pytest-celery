"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the :ref:`built-in-worker` vendor.
"""

from __future__ import annotations

import inspect
from types import ModuleType
from typing import Any

from celery import Celery
from celery.app.base import PendingConfiguration

from pytest_celery.vendors.worker.defaults import DEFAULT_WORKER_APP_NAME


class WorkerInitialContent:
    """This class is responsible for generating the initial content for the
    worker container volume.

    Responsibility Scope:
        Prepare the worker container with the required filesystem, configurations and
        dependencies for your project.
    """

    class Parser:
        """Parser for the initial content of the worker container."""

        def imports_str(self, modules: set[ModuleType]) -> str:
            """Parse the given modules and return a string with the import
            statements.

            Args:
                modules (set[ModuleType]): A set of modules to parse.

            Returns:
                str: "from module import \\*" statements.
            """
            return "".join(f"from {module.__name__} import *\n" for module in modules)

        def imports_src(self, modules: set[ModuleType]) -> dict:
            """Parse the given modules and return a dict with the source code
            of the modules.

            Args:
                modules (set[ModuleType]): A set of modules to parse.

            Returns:
                dict: A dict with the source code of the modules.
            """
            src = dict()
            for module in modules:
                src[f"{module.__name__.replace('.', '/')}.py"] = inspect.getsource(module).encode()
            return src

        def app_name(self, name: str | None = None) -> str:
            """Generates the Celery app initialization string.

            Args:
                name (str | None, optional): The app name. Defaults to None.

            Returns:
                str: app = Celery(name)
            """
            name = name or DEFAULT_WORKER_APP_NAME
            return f"app = Celery('{name}')"

        def config(self, app: Celery | None = None) -> str:
            """Generates the Celery app configuration changes.

            Args:
                app (Celery | None, optional): Celery app with possibly changed config. Defaults to None.

            Raises:
                TypeError: If the app.conf.changes property is not a dict.

            Returns:
                str: config = {key: value, ...} or config = None
            """
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
        """Creates an initial content for the worker container. Defaults to
        built-in plugin-provided modules.

        Args:
            app_module (ModuleType | None, optional): App module adjusted for parsing. Defaults to None.
            utils_module (ModuleType | None, optional): Utils module with for running python code in the
            worker container. Defaults to None.
        """
        self.parser = self.Parser()
        self._initial_content = {
            "__init__.py": b"",
            "imports": dict(),  # Placeholder item
        }
        self.set_app_module(app_module)
        self.set_utils_module(utils_module)
        self.set_app_name()
        self.set_config_from_object()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WorkerInitialContent):
            return False
        try:
            return self.generate() == other.generate()
        except ValueError:
            return all(
                [
                    self._app_module_src == other._app_module_src,
                    self._utils_module_src == other._utils_module_src,
                    self._initial_content == other._initial_content,
                    self._app == other._app,
                    self._config == other._config,
                ]
            )

    def set_app_module(self, app_module: ModuleType | None = None) -> None:
        """Injects an app module into the initial content."""
        self._app_module_src: str | None

        if app_module:
            self._app_module_src = inspect.getsource(app_module)
        else:
            self._app_module_src = None

    def set_utils_module(self, utils_module: ModuleType | None = None) -> None:
        """Injects a utils module into the initial content."""
        self._utils_module_src: str | None

        if utils_module:
            self._utils_module_src = inspect.getsource(utils_module)
        else:
            self._utils_module_src = None

    def add_modules(self, name: str, modules: set[ModuleType]) -> None:
        """Adds a set of modules to the initial content.

        Args:
            name (str): Arbitrary unique name for the set of modules.
            modules (set[ModuleType]): A set of modules to add.
        """
        if not name:
            raise ValueError("name cannot be empty")

        if not modules:
            raise ValueError("modules cannot be empty")

        self._initial_content["imports"][name] = self.parser.imports_str(modules)  # type: ignore
        self._initial_content.update(self.parser.imports_src(modules))

    def set_app_name(self, name: str | None = None) -> None:
        """Sets the Celery app name.

        Args:
            name (str | None, optional): The app name. Defaults to None.
        """
        name = name or DEFAULT_WORKER_APP_NAME
        self._app = self.parser.app_name(name)

    def set_config_from_object(self, app: Celery | None = None) -> None:
        """Sets the Celery app configuration from the given app.

        Args:
            app (Celery | None, optional): Celery app with possibly changed config. Defaults to None.
        """
        self._config = self.parser.config(app)

    def generate(self) -> dict:
        """Generates the initial content for the worker container.

        Returns:
            dict: Initial content volume for the worker container.
        """
        initial_content = self._initial_content.copy()
        initial_content["app.py"] = self._generate_app_py(initial_content)
        initial_content["utils.py"] = self._generate_utils_py()
        return initial_content

    def _generate_app_py(self, initial_content: dict) -> bytes:
        """Generates the app.py file for the worker container.

        Args:
            initial_content (dict): The current initial content.

        Returns:
            bytes: The generated app.py file.
        """
        if not self._app_module_src:
            raise ValueError("Please use set_app_module() to define the app module before generating initial content")

        if not initial_content["imports"]:
            raise ValueError(
                "Please use set_utils_module() to define the utils module before generating initial content"
            )

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
        """Generates the utils.py file for the worker container.

        Returns:
            bytes: The generated utils.py file.
        """
        if not self._utils_module_src:
            raise ValueError("Please set_utils_module() before generating initial content")

        return self._utils_module_src.encode()
