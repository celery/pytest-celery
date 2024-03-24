.. _default-tasks:

================
 Built-in Tasks
================

:Release: |version|
:Date: |today|

The plugin provides a list of built-in celery tasks that can be used out of the box. This page will
list all the available tasks.

.. tip::

    The tasks injected into the workers that use the default volume with:

    .. code-block:: python

        volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},

.. contents::
    :local:
    :depth: 1

add
===

.. versionadded:: 1.0.0

.. literalinclude:: ../../src/pytest_celery/vendors/worker/tasks.py
    :language: python
    :caption: pytest_celery.vendors.worker.tasks
    :start-after: # ------------- add -------------
    :end-before: # ------------- add_replaced -------------

add_replaced
============

.. versionadded:: 1.0.0

.. literalinclude:: ../../src/pytest_celery/vendors/worker/tasks.py
    :language: python
    :caption: pytest_celery.vendors.worker.tasks
    :start-after: # ------------- add_replaced -------------
    :end-before: # ------------- fail -------------

fail
====

.. versionadded:: 1.0.0

.. literalinclude:: ../../src/pytest_celery/vendors/worker/tasks.py
    :language: python
    :caption: pytest_celery.vendors.worker.tasks
    :start-after: # ------------- fail -------------
    :end-before: # ------------- identity -------------

identity
========

.. versionadded:: 1.0.0

.. literalinclude:: ../../src/pytest_celery/vendors/worker/tasks.py
    :language: python
    :caption: pytest_celery.vendors.worker.tasks
    :start-after: # ------------- identity -------------
    :end-before: # ------------- noop -------------

noop
====

.. versionadded:: 1.0.0

.. literalinclude:: ../../src/pytest_celery/vendors/worker/tasks.py
    :language: python
    :caption: pytest_celery.vendors.worker.tasks
    :start-after: # ------------- noop -------------
    :end-before: # ------------- ping -------------

ping
====

.. versionadded:: 1.0.0

.. literalinclude:: ../../src/pytest_celery/vendors/worker/tasks.py
    :language: python
    :caption: pytest_celery.vendors.worker.tasks
    :start-after: # ------------- ping -------------
    :end-before: # ------------- sleep -------------

sleep
=====

.. versionadded:: 1.0.0

.. literalinclude:: ../../src/pytest_celery/vendors/worker/tasks.py
    :language: python
    :caption: pytest_celery.vendors.worker.tasks
    :start-after: # ------------- sleep -------------
    :end-before: # ------------- xsum -------------

xsum
====

.. versionadded:: 1.0.0

.. literalinclude:: ../../src/pytest_celery/vendors/worker/tasks.py
    :language: python
    :caption: pytest_celery.vendors.worker.tasks
    :start-after: # ------------- xsum -------------
