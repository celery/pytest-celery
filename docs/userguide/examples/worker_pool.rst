.. _examples_worker_pool:

=============
 worker_pool
=============

:Release: |version|
:Date: |today|

.. contents::
    :local:
    :depth: 2

Description
===========

This example project demonstrates how to use a different `worker pool <https://docs.celeryq.dev/en/stable/reference/cli.html#cmdoption-celery-worker-P>`_.
The example uses two different methods to run the Celery worker with different pools.

The following guide will explain each method and how they are used.

.. tip::

    See first the :ref:`examples_myworker` example before continuing with this one.

Breakdown
=========

File Structure
~~~~~~~~~~~~~~

The following diagram lists the relevant files in the project.

.. code-block:: text

    rabbitmq_management/
    ├── tests/
    │   ├── __init__.py
    │   └── test_gevent_pool.py
    │   └── test_solo_pool.py
    └── Dockerfile
    └── tasks.py
    └── requirements.txt

Dockerfile
~~~~~~~~~~

To use the gevent pool, we create our own image using a similar Dockerfile to the one in the :ref:`examples_myworker` example.
The purpose of this worker is to ensure the gevent dependency is installed.

.. literalinclude:: ../../../examples/worker_pool/Dockerfile
   :language: docker
   :caption: examples.worker_pool.Dockerfile

.. literalinclude:: ../../../examples/worker_pool/requirements.txt
   :language: docker
   :caption: examples.worker_pool.requirements.txt

tasks.py
~~~~~~~~

Our tasks module is using the example task from the `Celery gevent example <https://github.com/celery/celery/blob/main/examples/gevent/README.rst>`_.

.. literalinclude:: ../../../examples/worker_pool/tasks.py
   :language: python
   :caption: examples.worker_pool.tasks.py

test_gevent_pool.py
~~~~~~~~~~~~~~~~~~~

To add a new gevent worker, we create a new :class:`CeleryWorkerContainer <pytest_celery.vendors.worker.container.CeleryWorkerContainer>` to
configure the worker with the gevent pool.

.. literalinclude:: ../../../examples/worker_pool/tests/test_gevent_pool.py
   :language: python
   :caption: examples.worker_pool.tests.test_gevent_pool.py
   :end-before: # ----------------------------

And then we can just use it in our tests.

.. literalinclude:: ../../../examples/worker_pool/tests/test_gevent_pool.py
   :language: python
   :caption: examples.worker_pool.tests.test_gevent_pool.py
   :start-after: # ----------------------------

test_solo_pool.py
~~~~~~~~~~~~~~~~~

The solo pool example on the other hand, reconfigures the default :ref:`built-in-worker`
as it does not require any additional dependencies.

.. literalinclude:: ../../../examples/worker_pool/tests/test_solo_pool.py
   :language: python
   :caption: examples.worker_pool.tests.test_solo_pool.py
