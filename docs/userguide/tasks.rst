.. _injecting-tasks:

==================
 How to add tasks
==================

:Release: |version|
:Date: |today|

The plugin uses its :ref:`code-generation` mechanism to inject tasks modules into the worker
container. The available tasks can be configured differently for each test case using the
`Fixture availability <https://docs.pytest.org/en/latest/reference/fixtures.html#fixture-availability>`_ feature of pytest.

This guide will teach you how to utilize this mechanism to add tasks for your Celery workers in your test cases.

.. contents::
    :local:
    :depth: 2

.. note::

    If you already understand how the initialization pipeline works, you can skip to the
    :ref:`tasks-modules-injection` section.

.. include:: ../includes/worker-breakdown.txt

.. _tasks-modules-injection:

Tasks modules injection
=======================

.. versionadded:: 1.0.0

To add you own tasks, use the :func:`default_worker_tasks <pytest_celery.vendors.worker.fixtures.default_worker_tasks>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_tasks(default_worker_tasks: set) -> set:
        from tests import tasks

        default_worker_tasks.add(tasks)
        return default_worker_tasks
