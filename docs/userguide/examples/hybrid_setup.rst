.. _examples_hybrid_setup:

==============
 hybrid_setup
==============

:Release: |version|
:Date: |today|

.. contents::
    :local:
    :depth: 2

Description
===========

The purpose of this example is to demonstrate a more complex setup with multiple components.
The example is using two brokers, with the failover feature, a backend and multiple workers of different pools and versions.
One of the workers is using gevent with the latest Celery release on the default queue,
while the other is using prefork with Celery 4 and its own queue.

It uses the following workflow to utilize both workers:

.. code-block:: python

    canvas = (
        group(
            identity.si("Hello, "),
            identity.si("world!"),
        )
        | noop.s().set(queue="legacy")
        | identity.si("Done!")
    )

Highlights
~~~~~~~~~~

1. No default components.
2. Session broker and backend components.
    - Shared between tests, but not between :pypi:`pytest-xdist <pytest-xdist>` sessions.
    - Only the workers are created again for each test case.
3. Injects tasks and signal handlers modules to all workers.

This example is based on,

- The :ref:`examples_myworker` example.
- The :ref:`examples_worker_pool` example.

Breakdown
=========

File Structure
~~~~~~~~~~~~~~

The following diagram lists the relevant files in the project.

.. code-block:: text

    hybrid_setup/
    ├── requirements.txt
    └── tests/
        ├── conftest.py
        ├── test_hybrid_setup.py
        └── vendors/
            ├── __init__.py
            ├── rabbitmq.py
            ├── redis_backend.py
            └── workers/
                ├── __init__.py
                ├── gevent.Dockerfile
                ├── gevent.py
                ├── legacy.Dockerfile
                ├── legacy.py
                ├── signals.py
                └── tasks.py

requirements.txt
~~~~~~~~~~~~~~~~

Take a look at the requirements file for this example:

.. literalinclude:: ../../../examples/hybrid_setup/requirements.txt
    :language: text
    :caption: examples.hybrid_setup.requirements.txt

Take note the :pypi:`gevent <gevent>` can be installed independently from the :pypi:`celery <celery>` package.

conftest.py
~~~~~~~~~~~

The ``conftest.py`` file will be used to aggregate each individual configuration. To understand how it works,
we'll split the file into three parts.

1. Creating the docker network for the components.
2. Configuring the broker, backend and workers for the setup.
3. Injecting the tasks and signal handlers modules.

.. literalinclude:: ../../../examples/hybrid_setup/tests/conftest.py
    :language: python
    :caption: examples.hybrid_setup.tests.conftest.py
    :start-after: # ----------------------------

test_hybrid_setup.py
~~~~~~~~~~~~~~~~~~~~

Every test case that uses the :func:`celery_setup <pytest_celery.fixtures.setup.celery_setup>` fixture will run
its scenario on the setup that was configured in the ``conftest.py`` file.

For this example, we have the following test cases.

.. literalinclude:: ../../../examples/hybrid_setup/tests/test_hybrid_setup.py
    :language: python
    :caption: examples.hybrid_setup.tests.test_hybrid_setup.py
    :start-after: TestHybridSetupExample

.. tip::

    The components themselves can be used in the test case to easily access their attributes and methods, like shown
    in the failover test case. When used without the :func:`celery_setup <pytest_celery.fixtures.setup.celery_setup>`
    fixture, the components will run independently and might not be aware of each other.

rabbitmq.py and redis_backend.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The brokers and result backend are defined as independent components that are being configured into the setup
using the ``conftest.py`` file. They add **session scope** fixtures and integrate using the matching :ref:`node class <test-nodes>`.

Main | Failover Brokers
-----------------------

.. literalinclude:: ../../../examples/hybrid_setup/tests/vendors/rabbitmq.py
    :language: python
    :caption: examples.hybrid_setup.tests.vendors.rabbitmq.py

Result Backend
--------------

.. literalinclude:: ../../../examples/hybrid_setup/tests/vendors/redis_backend.py
    :language: python
    :caption: examples.hybrid_setup.tests.vendors.redis_backend.py

gevent.py and gevent.Dockerfile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These files are taken from the :ref:`test_gevent_pool` example with one simple change.

.. code-block:: python

    RUN pip install "celery[gevent]" "pytest-celery[all]==1.0.0"

The Dockerfile doesn't use the requirements file, but instead installs the packages directly.

.. literalinclude:: ../../../examples/hybrid_setup/tests/vendors/workers/gevent.Dockerfile
    :language: docker
    :caption: examples.hybrid_setup.tests.vendors.workers.gevent.Dockerfile

.. note::

    The :ref:`test_gevent_pool` example defines everything in the test file. Here we use the ``gevent.py`` file.

.. literalinclude:: ../../../examples/hybrid_setup/tests/vendors/workers/gevent.py
    :language: python
    :caption: examples.hybrid_setup.tests.vendors.workers.gevent.py

legacy.py and legacy.Dockerfile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The "legacy" worker is basically Celery 4 worker with the prefork pool. Very similar to the gevent worker,
we add a new Dockerfile and worker module.

.. literalinclude:: ../../../examples/hybrid_setup/tests/vendors/workers/legacy.Dockerfile
    :language: docker
    :caption: examples.hybrid_setup.tests.vendors.workers.legacy.Dockerfile

.. literalinclude:: ../../../examples/hybrid_setup/tests/vendors/workers/legacy.py
    :language: python
    :caption: examples.hybrid_setup.tests.vendors.workers.legacy.py

.. tip::

    Check all of the configurations above again and notice the usage of ``hybrid_setup_example_network``.
    See how both session and non-session fixtures are sharing the same session docker network.

tasks.py and signals.py
~~~~~~~~~~~~~~~~~~~~~~~

The tasks and signal handlers are being injected into the workers using the ``conftest.py`` file,
according to the documentation:

1. :ref:`injecting-tasks`.
2. :ref:`injecting-signals-handlers`.

The files themselves are very simple,

.. literalinclude:: ../../../examples/hybrid_setup/tests/vendors/workers/tasks.py
    :language: python
    :caption: examples.hybrid_setup.tests.vendors.workers.tasks.py

.. literalinclude:: ../../../examples/hybrid_setup/tests/vendors/workers/signals.py
    :language: python
    :caption: examples.hybrid_setup.tests.vendors.workers.signals.py

And again, from ``confest.py``,

.. code-block:: python

    @pytest.fixture
    def default_worker_tasks(default_worker_tasks: set) -> set:
        from tests.vendors.workers import tasks

        default_worker_tasks.add(tasks)
        return default_worker_tasks


    @pytest.fixture
    def default_worker_signals(default_worker_signals: set) -> set:
        from tests.vendors.workers import signals

        default_worker_signals.add(signals)
        return default_worker_signals

.. note::

    The tasks and signals are being injected into the workers that use the default volume with:

    .. code-block:: python

        volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},

    Both our workers are using the default volume, so we only need to inject the tasks and signals once.
