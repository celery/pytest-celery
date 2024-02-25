.. _tasks:

================================
 How to connect signal handlers
================================

:Release: |version|
:Date: |today|

Signal handlers may be defined in the publisher or the consumer side or both. When done
on the publisher side, they can be connected inside the scope of the test function using the
`standard Celery API <https://docs.celeryq.dev/en/stable/userguide/signals.html>`_. When done on the
consumer side, they can be connected using injected signal handlers modules, which we'll cover in this guide.

The plugin uses its :ref:`code-generation` mechanism to inject signal handlers modules into the worker
container. The available signal handlers can be configured differently for each test case using the
`Fixture availability <https://docs.pytest.org/en/latest/reference/fixtures.html#fixture-availability>`_ feature of pytest.

This guide will teach you how to utilize this mechanism to connect signal handlers to your Celery workers in your test cases.

.. contents::
    :local:
    :depth: 2

.. note::

    If you already understand how the initialization pipeline works, you can skip to the
    :ref:`signal-handlers-modules-injection` section.

.. include:: ../includes/worker-breakdown.txt

.. _signal-handlers-modules-injection:

Signal handlers modules injection
=================================

.. versionadded:: 1.0.0

To add your own signal handlers, use the :func:`default_worker_signals <pytest_celery.vendors.worker.fixtures.default_worker_signals>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_signals(default_worker_signals: set) -> set:
        from tests import signals

        default_worker_signals.add(signals)
        return default_worker_signals

For example, we can review the plugin's tests to see how the signal handlers are connected.

signals.py
~~~~~~~~~~

This module contain our signal handlers which we want to connect on the consumer side.

.. literalinclude:: ../../tests/smoke/signals.py
   :language: python
   :caption: tests.smoke.signals
   :start-after: from __future__ import annotations

test_signals.py
~~~~~~~~~~~~~~~

These tests demonstrate how to query the output of the signal handlers that were
injected into the worker container alongside inline signal handlers connected on the publisher side.

.. literalinclude:: ../../tests/smoke/test_signals.py
   :language: python
   :caption: tests.smoke.test_signals
   :start-after: class test_signals
