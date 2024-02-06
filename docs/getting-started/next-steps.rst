.. _next-steps:

============
 Next Steps
============

:Release: |version|
:Date: |today|

The :ref:`first-steps` guide introduced the basic concepts of the pytest-celery plugin.
As with any tutorial, it is recommended to first try out what you have learned before moving on to the next steps.
Be sure to review the :ref:`examples` for a breakdown of the usage and attempt running the :ref:`hello-world` example
to get a feel for the plugin before moving on to the advanced features.

This guide will cover advanced features of the plugin, which might only be relevant to some users at first. It will focus
on the mechanics of integrating the plugin with your own tech stack, and will be based on the material covered in the :ref:`first-steps` guide.

It is highly recommended to study well the :ref:`essential_resources` to better understand the engine that powers the pytest-celery plugin.

.. contents::
    :local:
    :depth: 2

.. _code-generation:

Code Generation
===============

The Celery worker container is being created with a special volume that contains testing infrastructure code, in addition to
the tasks modules and signal handlers modules that are being injected into the worker container from the test environment. It uses
strightforward regeneration of the code, to inject testing infrastructure into the worker container at runtime.

Initial Content
~~~~~~~~~~~~~~~

The :class:`WorkerInitialContent <pytest_celery.vendors.worker.volume.WorkerInitialContent>` class is responsible for generating
the initial content of the worker volume. It is used to parse the injected infrastructure and generate a dictionary of files for the
initial content of the worker container volume using :func:`WorkerInitialContent.generate() <pytest_celery.vendors.worker.volume.WorkerInitialContent.generate>`.

The code generation mechanism is responsible for injecting the following modules into the worker container.

app.py
~~~~~~

The :ref:`built-in-worker` uses the following ``app.py`` module to create the Celery application and uses
the ``/app`` directory to store the generated code.

.. _content-app:

.. literalinclude:: ../../src/pytest_celery/vendors/worker/content/app.py
   :language: python
   :caption: pytest_celery.vendors.worker.content.app

.. note::

    The ``app.py`` module is supplied with plugin but can be overridden with a custom module by the user.

utils.py
~~~~~~~~

The plugin injects a helper ``utils.py`` module to allow running testing infrastructure code within the worker container context.

.. literalinclude:: ../../src/pytest_celery/vendors/worker/content/utils.py
   :language: python
   :caption: pytest_celery.vendors.worker.content.utils

See :func:`CeleryTestWorker.get_running_processes_info() <pytest_celery.api.worker.CeleryTestWorker.get_running_processes_info>`
for an example of how the ``utils.py`` module is used.

.. note::

    The ``utils.py`` module is supplied with plugin but can be overridden with a custom module by the user.

Tasks modules
~~~~~~~~~~~~~

Tasks modules are being defined using the :func:`default_worker_tasks <pytest_celery.vendors.worker.fixtures.default_worker_tasks>` fixture.
The tasks modules will be reconstructed inside the volume with the same structure as the test environment to avoid python import errors.

Use the following snippet to add tasks modules to the worker container:

.. code-block:: python

    @pytest.fixture
    def default_worker_tasks(default_worker_tasks: set) -> set:
        from tests import tasks

        default_worker_tasks.add(tasks)
        return default_worker_tasks

Signal handlers
~~~~~~~~~~~~~~~

Celery signal handlers are divided into two groups. The first group is the signal handlers that are being used within the test code,
and the second group is the signal handlers that are being injected into the worker container.

Inline signal handlers
----------------------

Signal handlers that are being registered on the Celery publisher side, are defined within the test code.

.. code-block:: python

    from celery.signals import before_task_publish
    from celery.signals import after_task_publish

    def test_before_task_publish(celery_setup: CeleryTestSetup):
        @before_task_publish.connect
        def before_task_publish_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        signal_was_called = False
        mytask.s().apply_async()
        assert signal_was_called is True

    def test_after_task_publish(self, celery_setup: CeleryTestSetup):
        @after_task_publish.connect
        def after_task_publish_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        signal_was_called = False
        mytask.s().apply_async()
        assert signal_was_called is True

Injected signal handlers
------------------------

Signal handlers that are being registered on the Celery consumer side, are being injected into the worker container
using the :func:`default_worker_signals <pytest_celery.vendors.worker.fixtures.default_worker_signals>` fixture,
similar to the tasks modules.

.. code-block:: python

    @pytest.fixture
    def default_worker_signals(default_worker_signals: set) -> set:
        from tests import signals

        default_worker_signals.add(signals)
        return default_worker_signals

For example, such ``signals.py`` module might look like this:

.. code-block:: python

    from celery.signals import worker_init


    @worker_init.connect
    def worker_init_handler(sender, **kwargs):
        print("worker_init_handler")

Celery app
~~~~~~~~~~

The provided :ref:`app.py <content-app>` uses the `config_from_object() <https://docs.celeryq.dev/en/main/userguide/application.html#config-from-object>`_
and `app.conf.changes <https://docs.celeryq.dev/en/main/userguide/application.html#configuration>`_ to transmit the configuration
from the test environment to the worker container.

The ``app.conf`` is set like this when the worker is booting up:

.. code-block:: python

    config = None

    if config:
        app.config_from_object(config)
        print(f"Changed worker configuration: {json.dumps(config, indent=4)}")

The ``config = None`` will be set on the fly with a dictionary of the modified configuration based on ``app.conf.changes``,
or remain ``None`` if no changes are made to ``app.conf``.

.. warning::

    The volume creation is done at the ``session`` scope even though the ``default_worker_app`` is not using the ``session`` scope directly,
    and may not be modified during the test run itself. To customize the configuration, hook into ``default_worker_app`` like shown :ref:`here <celery-application>`.

Mounting ``src``
~~~~~~~~~~~~~~~~

To access your project's source code from the worker container, you can mount your code to the the ``/src`` directory like this:

.. code-block:: python

    default_worker_container = container(
        ...
        volumes={
            "{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME,
            os.path.abspath(os.getcwd()): {
                "bind": "/src",
                "mode": "rw",
            },
        },
        ...
    )

For a working example, see the :ref:`examples_django` example or the official Celery smoke tests `dev container <https://github.com/celery/celery/blob/main/t/smoke/workers/dev.py>`_,
which builds the Celery worker from the local source code.

.. _architecture-injection:

Architecture Injection
======================

Every Celery based project has its own tech stack, and the plugin is designed to be flexible enough to accommodate most standard tech stacks.
The :ref:`built-in components <built-in-components>` provides a starting platform for replacing the default components with your own.

To inject your own architecture, implement every :ref:`layer <components-layers>` of the the built-in component you want to replace.

We will use the :ref:`examples_myworker` example to demonstrate how to do exactly that and replace the built-in worker with a custom one.

Custom Component
~~~~~~~~~~~~~~~~

We'll use the following Dockerfile to create a custom worker container to replace the built-in worker component.

.. literalinclude:: ../../examples/myworker/tests/myworker/Dockerfile
   :language: docker
   :caption: examples.myworker.tests.myworker.Dockerfile

Then, we'll create our own :class:`CeleryWorkerContainer <pytest_celery.vendors.worker.container.CeleryWorkerContainer>` class.

.. code-block:: python

    class MyWorkerContainer(CeleryWorkerContainer):
        @property
        def client(self) -> Any:
            return self

        @classmethod
        def version(cls) -> str:
            return "Celery main branch"

        @classmethod
        def log_level(cls) -> str:
            return "INFO"

        @classmethod
        def worker_name(cls) -> str:
            return "my_worker"

        @classmethod
        def worker_queue(cls) -> str:
            return "myworker"

And build our container using the standard `pytest-docker-tools <https://pypi.org/project/pytest-docker-tools>`_ API.

.. code-block:: python

    myworker_image = build(
        path=".",
        dockerfile="tests/myworker/Dockerfile",
        tag="pytest-celery/myworker:example",
        buildargs=MyWorkerContainer.buildargs(),
    )


    myworker_container = container(
        image="{myworker_image.id}",
        environment=fxtr("default_worker_env"),
        network="{default_pytest_celery_network.name}",
        volumes={"{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME},
        wrapper_class=MyWorkerContainer,
        timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
    )

Pytest Integration
------------------

To inject the new container into the plugin, you need to use a simple pattern to create a pytest fixture
that represents the new component.

.. code-block:: python

    @pytest.fixture
    def new_component_name(new_component_container):
        node: CeleryTestNode = NewComponent(myworker_container)
        yield node
        node.teardown()

So for our example, we would use the following fixture:

.. code-block:: python

    @pytest.fixture
    def myworker_worker(myworker_container: MyWorkerContainer, celery_setup_app: Celery) -> CeleryTestWorker:
        worker = CeleryTestWorker(myworker_container, app=celery_setup_app)
        yield worker
        worker.teardown()

Notice the additional ``celery_setup_app: Celery`` fixture. It is used to initialize the worker container with our Celery app instance.

.. tip::

    You may use additional fixtures when creating new components to create a more complex setup pipeline for the new component.

Setup Integration
-----------------

Lastly, you need to integrate the new component into the setup pipeline according to its role in the architecture. As
:ref:`discussed before <test-clusters>`, components are loaded using the appropriate cluster fixture.

As we're replacing the worker component, we use the :func:`celery_worker_cluster <pytest_celery.fixtures.worker.celery_worker_cluster>` to
add it to the setup.

.. code-block:: python

    @pytest.fixture
    def celery_worker_cluster(celery_worker: CeleryTestWorker, myworker_worker: CeleryTestWorker) -> CeleryWorkerCluster:
        cluster = CeleryWorkerCluster(celery_worker, myworker_worker)
        yield cluster
        cluster.teardown()

This code will add a new worker to the default worker cluster. The workers will be aware of each other and will share
the same docker network and Celery app instance.

To access the new worker, you can use the :func:`celery_setup <pytest_celery.fixtures.setup.celery_setup>` fixture.

.. code-block:: python

    def test_myworker(celery_setup: CeleryTestSetup):
        assert celery_setup.worker_cluster[1].ready()

Or using a context manager:

.. code-block:: python

    def test_myworker(celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            assert worker.ready()

The default worker will be using the default ``celery`` queue.
Our new worker will be using the ``myworker`` queue, as defined before:

.. code-block:: python

    @classmethod
    def worker_queue(cls) -> str:
        return "myworker"

Remove the ``worker_queue()`` implementation completely from ``MyWorkerContainer`` to fallback to the default ``celery`` queue with our new worker as well.

.. tip::

    See :ref:`examples_rabbitmq-management` example for replacing the default broker.

    See :ref:`examples_range` example for replacing the worker cluster with a dynamic number of workers.

    See `Celery smoke tests workers <https://github.com/celery/celery/tree/main/t/smoke/workers>`_ for production examples.

Where to go from here
=====================

If you want to learn more you should continue to the :ref:`User Guide <userguide>`.
