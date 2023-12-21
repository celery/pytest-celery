from __future__ import annotations

import inspect
from types import ModuleType

import pytest
from celery import Celery

import pytest_celery
from pytest_celery import DEFAULT_WORKER_APP_NAME
from pytest_celery import WorkerInitialContent


class test_worker_initial_content:
    @pytest.mark.parametrize("parser", [WorkerInitialContent.Parser()])
    class test_parser:
        @pytest.mark.parametrize(
            "modules",
            [
                set(),
                {pytest},
                {pytest, pytest_celery},
            ],
        )
        class test_imports:
            def test_imports_str(self, parser: WorkerInitialContent.Parser, modules: set[ModuleType]):
                assert parser.imports_str(modules) == "".join(
                    f"from {module.__name__} import *\n" for module in modules
                )

            def test_imports_src(self, parser: WorkerInitialContent.Parser, modules: set[ModuleType]):
                assert parser.imports_src(modules) == {
                    f"{module.__name__.replace('.', '/')}.py": inspect.getsource(module).encode() for module in modules
                }

        @pytest.mark.parametrize(
            "name",
            [
                None,
                "app",
                "test_app",
            ],
        )
        def test_app_name(self, parser: WorkerInitialContent.Parser, name: str):
            assert parser.app_name(name) == f"app = Celery('{name or DEFAULT_WORKER_APP_NAME}')"

        @pytest.mark.parametrize(
            "app,config",
            [
                (None, None),
                (Celery("test"), None),
                (Celery(), {"broker_url": "420"}),
            ],
        )
        def test_config(self, parser: WorkerInitialContent.Parser, app: Celery | None, config: dict | None):
            if app and config:
                app.conf.update(config)

            if config:
                changes = (f"\t{repr(key)}: {repr(value)}" for key, value in config.items())
                expected_config = "config = {\n" + ",\n".join(changes) + "\n}" if changes else "config = None"
            else:
                expected_config = "config = None"

            assert parser.config(app) == expected_config

    def test_init(self):
        actual_content = WorkerInitialContent()
        assert isinstance(actual_content.parser, WorkerInitialContent.Parser)
        assert actual_content._initial_content == {
            "__init__.py": b"",
            "imports": dict(),
        }
        assert actual_content._app == f"app = Celery('{DEFAULT_WORKER_APP_NAME}')"
        assert actual_content._config == "config = None"

    def test_eq(self):
        from pytest_celery.vendors.worker.content import app as app_module

        actual_content = WorkerInitialContent()

        assert actual_content == WorkerInitialContent()
        assert actual_content == actual_content

        actual_content.set_app_module(app_module)
        actual_content.add_modules("pytest", {pytest})
        assert actual_content != WorkerInitialContent()

    def test_set_app_module(self):
        from pytest_celery.vendors.worker.content import app as app_module

        actual_content = WorkerInitialContent()

        actual_content.set_app_module(app_module)
        assert actual_content._app_module_src == inspect.getsource(app_module)

        actual_content.set_app_module(None)
        assert actual_content._app_module_src is None

    @pytest.mark.parametrize(
        "modules",
        [
            {
                "pytest": {pytest},
            },
            {
                "pytest": {pytest},
                "pytest_celery": {pytest_celery},
            },
            {
                "pytest": {pytest, pytest_celery},
                "pytest_celery": {pytest, pytest_celery},
            },
        ],
    )
    def test_add_modules(self, modules: dict[str, set[ModuleType]]):
        from pytest_celery.vendors.worker.content import app as app_module

        actual_content = WorkerInitialContent()

        expected_content = WorkerInitialContent()
        actual_content.set_app_module(app_module)
        expected_content.set_app_module(app_module)

        for module_name, module_set in modules.items():
            actual_content.add_modules(module_name, module_set)

        actual_intial_content = actual_content._initial_content
        assert "imports" in actual_intial_content
        assert modules.keys() == actual_intial_content["imports"].keys()

        for module_name, modules_set in modules.items():
            expected_content._initial_content["imports"][module_name] = actual_content.parser.imports_str(modules_set)
            expected_content._initial_content.update(actual_content.parser.imports_src(modules_set))

        assert actual_content == expected_content

    def test_set_app_name(self):
        actual_content = WorkerInitialContent()

        actual_content.set_app_name()
        assert actual_content._app == f"app = Celery('{DEFAULT_WORKER_APP_NAME}')"

        actual_content.set_app_name("test")
        assert actual_content._app == "app = Celery('test')"

    def test_set_config_from_object(self):
        actual_content = WorkerInitialContent()

        actual_content.set_config_from_object()
        assert actual_content._config == "config = None"

        actual_content.set_config_from_object(Celery("test"))
        assert actual_content._config == "config = None"

        actual_content.set_config_from_object(Celery("test", broker_url="420"))
        assert actual_content._config == "config = {\n\t'broker_url': '420'\n}"

    class test_generate:
        def test_generate_default(self):
            actual_content = WorkerInitialContent()

            with pytest.raises(ValueError):
                actual_content.generate()

        @pytest.mark.parametrize(
            "app",
            [
                None,
                Celery("test"),
                Celery("test", broker_url="420"),
            ],
        )
        def test_generate(self, app: Celery | None):
            from pytest_celery.vendors.worker.content import app as app_module

            actual_content = WorkerInitialContent()

            actual_content.set_app_module(app_module)
            actual_content.add_modules("tests_modules", {pytest, pytest_celery})
            actual_content.set_config_from_object(app)

            expected_content = WorkerInitialContent(app_module)
            expected_content.add_modules("tests_modules", {pytest, pytest_celery})
            expected_content.set_config_from_object(app)

            assert actual_content.generate() == expected_content.generate()
