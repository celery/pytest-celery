.. _vendors:

=========
 Vendors
=========

:Release: |version|
:Date: |today|

.. contents::
    :local:
    :depth: 2

Built-in Brokers and Backends
=============================

The plugin comes with support for several brokers and backends out of
the box.  This page lists the supported vendors and their status.

Brokers
~~~~~~~

+---------------+--------------+--------------+
| **Name**      | **Status**   | **Enabled**  |
+---------------+--------------+--------------+
| *RabbitMQ*    | Stable       | Yes          |
+---------------+--------------+--------------+
| *Redis*       | Stable       | Yes          |
+---------------+--------------+--------------+

Backends
~~~~~~~~

+---------------+--------------+--------------+
| **Name**      | **Status**   | **Enabled**  |
+---------------+--------------+--------------+
| *Redis*       | Stable       | Yes          |
+---------------+--------------+--------------+
| *Memcache*    | Experimental | No           |
+---------------+--------------+--------------+

Experimental brokers may be functional but are not confirmed to be
production ready.

Enabled means that it is automatically added to the test setup matrix
when running the test suite :ref:`if the vendor dependencies are installed <installation>`.

.. warning::

    Enabling a new vendor will automatically add it globally to every test suite that relies
    on the default vendors detection. Be careful when enabling new vendors and make sure they are
    stable and production ready.

.. _built-in-worker:

Built-in Celery Worker
======================

The plugin provides a built-in Celery worker that can be used to run
tests against. It uses the latest stable version of Celery and can be used, replaced or extended
by the user.

The Dockerfile is published with the source code and can be found using
:const:`WORKER_DOCKERFILE_ROOTDIR <pytest_celery.vendors.worker.defaults.WORKER_DOCKERFILE_ROOTDIR>`.

.. literalinclude:: ../../src/pytest_celery/vendors/worker/Dockerfile
   :language: docker
   :caption: pytest_celery.vendors.worker.Dockerfile

Custom Vendors
==============

Injected brokers, backends and workers can extend the built-in ones or
provide completely new ones. The plugin provides a set of base classes
that can be used to implement custom vendors.

Custom Broker
~~~~~~~~~~~~~

.. autoclass:: pytest_celery.api.broker.CeleryTestBroker
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :no-index:

Custom Backend
~~~~~~~~~~~~~~

.. autoclass:: pytest_celery.api.backend.CeleryTestBackend
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :no-index:

Custom Worker
~~~~~~~~~~~~~

.. autoclass:: pytest_celery.api.worker.CeleryTestWorker
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :no-index:
