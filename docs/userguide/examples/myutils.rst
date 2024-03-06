.. _examples_myutils:

=========
 myutils
=========

:Release: |version|
:Date: |today|

.. contents::
    :local:
    :depth: 2

Description
===========

This example project shows :ref:`utils-module` to add custom APIs to the ``utils.py`` module
that is being injected into the worker container.

Breakdown
=========

File Structure
~~~~~~~~~~~~~~

The following diagram lists the relevant files in the project.

.. code-block:: text

    myutils/
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── myutils.py
    │   └── test_myutils.py
    └── requirements.txt

myutils.py
~~~~~~~~~~

For this example, we'll add a ``myfunc()`` using our own ``myutils.py`` module.

.. code-block:: python

    from pytest_celery.vendors.worker.content.utils import get_running_processes_info  # noqa


    def myfunc():
        return "foo"

.. note::
    The ``get_running_processes_info`` function is imported from the original ``utils.py`` module,
    which means the plugin need to be installed in the worker container. Otherwise, you may provide
    your own implementation.

conftest.py
~~~~~~~~~~~

To inject our own module, we use the :func:`default_worker_utils_module <pytest_celery.vendors.worker.fixtures.default_worker_utils_module>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_utils_module() -> ModuleType:
        from tests import myutils

        return myutils

.. warning::
    The module will be renamed inside the worker container as ``utils.py``, regardless of the name of the module you provide.

Then, we create an API to access the ``myfunc()`` function from the testing environment.

.. code-block:: python

    class MyWorker(CeleryTestWorker):

        def myfunc(self) -> bool:
            exit_code, output = self.container.exec_run(
                'python -c "from utils import myfunc; print(myfunc())"',
            )
            if exit_code != 0:
                raise RuntimeError(f"Error: {output}")
            output = output.decode("utf-8")
            return output.strip()


    @pytest.fixture
    def default_worker_cls() -> type[CeleryTestWorker]:
        return MyWorker

Which uses the new ``myfunc()`` function from the provided ``myutils.py`` module.

test_myutils.py
~~~~~~~~~~~~~~~

Our test file tests the new ``myfunc()`` function in three different ways.

Directly.

.. code-block:: python

    def test_myfunc():
        assert myfunc() == "foo"

Using a single worker component.

.. code-block:: python

    def test_myfunc_in_worker(celery_worker: MyWorker):
        assert celery_worker.myfunc() == "foo"
        assert celery_worker.get_running_processes_info()

Using a full setup.

.. code-block:: python

    def test_myfunc_in_setup_worker(celery_setup: CeleryTestSetup):
        celery_worker: MyWorker = celery_setup.worker
        assert celery_worker.myfunc() == "foo"
        assert celery_worker.get_running_processes_info()
