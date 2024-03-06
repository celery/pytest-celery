.. _utils-module:

==========================================
 How to inject your own utility functions
==========================================

:Release: |version|
:Date: |today|

The plugin injects a special ``utils.py`` module into the worker component to provide
enhanced testing capabilities over the Celery worker component. The module contains API that is accessible using the
:class:`CeleryTestWorker API <pytest_celery.api.worker.CeleryTestWorker>`.

This guide will teach you how to inject your own utility functions into the worker component
using this mechanism.

.. contents::
    :local:
    :depth: 2

.. note::

    If you already understand how the initialization pipeline works, you can skip to the
    :ref:`custom-utility-functions` section.

.. include:: ../includes/worker-breakdown.txt

.. _custom-utility-functions:

Custom Utility Functions
========================

.. versionadded:: 1.0.0

To configure your own module, use the :func:`default_worker_utils_module <pytest_celery.vendors.worker.fixtures.default_worker_utils_module>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_utils_module() -> ModuleType:
        from tests import myutils

        return myutils

This will inject the ``myutils`` module into the worker component, **instead of the default module**,
allowing you to access your own utility functions.

.. warning::

    The module must provide all of the existing API in the ``utils.py`` module, otherwise
    the worker component will not function correctly (when based off of
    :class:`CeleryTestWorker <pytest_celery.api.worker.CeleryTestWorker>`).

For reference, the default ``utils.py`` module is defined as follows:

.. literalinclude:: ../../src/pytest_celery/vendors/worker/content/utils.py
   :language: python
   :caption: pytest_celery.vendors.worker.content.utils.py

.. tip::

    Check out the :ref:`examples_myutils` example for a demonstration of how to use this feature.
