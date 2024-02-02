.. _examples_myworker:

==========
 myworker
==========

.. contents::
    :local:
    :depth: 2

Description
===========

This example project demonstrates how to inject a custom Celery worker into the testing environment.

Breakdown
=========

File Structure
~~~~~~~~~~~~~~

The following diagram lists the relevant files in the project.

.. code-block:: text

    myworker/
    ├── tests/
    │   ├── myworker/
    │   │   └── __init__.py
    │   │   └── Dockerfile.py
    │   │   └── myworker.py
    │   ├── __init__.py
    │   ├── conftest.py
    │   └── test_myworker.py
    └── requirements.txt

tests/myworker
~~~~~~~~~~~~~~

The ``tests/myworker`` package contains the custom Celery worker that will be injected into the testing environment.
It uses a simple Dockerfile to build the latest Celery version from git.

Dockerfile
~~~~~~~~~~

.. code-block:: docker

    FROM python:3.11-bookworm

``test_user`` is created to run the worker.

.. code-block:: docker

    # Create a user to run the worker
    RUN adduser --disabled-password --gecos "" test_user

    # Install system dependencies
    RUN apt-get update && apt-get install -y build-essential git

``CELERY_LOG_LEVEL``, ``CELERY_WORKER_NAME`` and ``CELERY_WORKER_QUEUE`` are set as build arguments.
These will be used to configure the worker for the tests.

.. code-block:: docker

    # Set arguments
    ARG CELERY_LOG_LEVEL=INFO
    ARG CELERY_WORKER_NAME=my_worker
    ARG CELERY_WORKER_QUEUE=celery
    ENV LOG_LEVEL=$CELERY_LOG_LEVEL
    ENV WORKER_NAME=$CELERY_WORKER_NAME
    ENV WORKER_QUEUE=$CELERY_WORKER_QUEUE

``/src`` is arbitrarily chosen as the working directory to install Celery from.

.. code-block:: docker

    # Install packages
    WORKDIR /src

    COPY --chown=test_user:test_user requirements.txt .
    RUN pip install --no-cache-dir --upgrade pip
    RUN pip install -r ./requirements.txt
    RUN git clone https://github.com/celery/celery.git

    WORKDIR /src/celery

    RUN pip install -e .

``/app`` is used internally by the pytest-celery plugin to inject code into the Celery worker at runtime.

.. code-block:: docker

    # The workdir must be /app
    WORKDIR /app

    # Switch to the test_user
    USER test_user

``CMD`` is set to allow standalone execution of the worker outside of the testing environment.
It is also useful for the injection of the worker as it removes the need to programmatically set the command.

.. code-block:: docker

    # Start the celery worker
    CMD celery -A app worker --loglevel=$LOG_LEVEL -n $WORKER_NAME@%h -Q $WORKER_QUEUE

myworker.py
~~~~~~~~~~~

The :class:`MyWorkerContainer` class is used to configure the worker container and acts as the interface
to the container instance.

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

Next, we build our worker image using the `build <https://github.com/Jc2k/pytest-docker-tools?tab=readme-ov-file#images>`_
and `container <https://github.com/Jc2k/pytest-docker-tools?tab=readme-ov-file#containers>`_ fixtures.

Notice we use default fixtures for other configuration options, notably the network and volume,
which allows the plugin to manage the lifecycle of these resources automatically.

These fixtures may be overridden if required.

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

Lastly, we wrap the container in a fixture to allow it to be injected into the test environment
using the :class:`CeleryTestWorker <pytest_celery.api.worker.CeleryTestWorker>` to represent the worker component.

.. code-block:: python

    @pytest.fixture
    def myworker_worker(myworker_container: MyWorkerContainer, celery_setup_app: Celery) -> CeleryTestWorker:
        worker = CeleryTestWorker(myworker_container, app=celery_setup_app)
        yield worker
        worker.teardown()

test_myworker.py
~~~~~~~~~~~~~~~~

To inject the worker into this test suite, we hook into the :func:`celery_worker_cluster <pytest_celery.fixtures.worker.celery_worker_cluster>` fixture
and add the worker to the cluster, alongside the default built-in worker.

.. code-block:: python

    @pytest.fixture
    def celery_worker_cluster(
        celery_worker: CeleryTestWorker,
        myworker_worker: CeleryTestWorker,
    ) -> CeleryWorkerCluster:
        cluster = CeleryWorkerCluster(celery_worker, myworker_worker)
        yield cluster
        cluster.teardown()

The default worker can also be fully replaced:

.. code-block:: python

    @pytest.fixture
    def celery_worker_cluster(
        myworker_worker: CeleryTestWorker,
    ) -> CeleryWorkerCluster:
        cluster = CeleryWorkerCluster(myworker_worker)
        yield cluster
        cluster.teardown()

And all that's left is the test itself, which is a simple :func:`ping <pytest_celery.vendors.worker.tasks.ping>`
test for each worker node in the cluster.

.. code-block:: python

    def test_ping(celery_setup: CeleryTestSetup):
        worker: CeleryTestWorker
        for worker in celery_setup.worker_cluster:
            sig: Signature = ping.s()
            res: AsyncResult = sig.apply_async(queue=worker.worker_queue)
            assert res.get(timeout=RESULT_TIMEOUT) == "pong"
