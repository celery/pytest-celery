.. _examples_django:

========
 django
========

:Release: |version|
:Date: |today|

.. contents::
    :local:
    :depth: 2

Description
===========

This example project demonstrates how to test the `official Celery django example <https://github.com/celery/celery/tree/main/examples/django>`_
using pytest-celery. For more about Django and Celery, please see the `official documentation <https://docs.celeryq.dev/en/stable/django/index.html>`_.

For the purposes of this example, we will focus on the setup and configuration side of things.

.. warning::
    Django support is currently experimental. Please :ref:`report <help>` any issues you encounter.

Breakdown
=========

File Structure
~~~~~~~~~~~~~~

The following diagram lists the relevant files in the project.

.. code-block:: text

    django/
    ├── demoapp/
    │   ├── tasks.py
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py
    │   └── DjangoWorker.Dockerfile
    │   └── test_tasks.py
    └── requirements.txt

DjangoWorker.Dockerfile
~~~~~~~~~~~~~~~~~~~~~~~

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

    EXPOSE 5678

``/src`` is arbitrarily chosen as the working directory to install the Django project from.

.. code-block:: docker

    # Install packages
    WORKDIR /src

    COPY --chown=test_user:test_user requirements.txt .
    RUN pip install --no-cache-dir --upgrade pip
    RUN pip install -r ./requirements.txt

    # Switch to the test_user
    USER test_user

    # Start the celery worker
    CMD celery -A proj worker --loglevel=$LOG_LEVEL -n $WORKER_NAME@%h -Q $WORKER_QUEUE

conftest.py
~~~~~~~~~~~

The :class:`DjangoWorkerContainer` class is used to configure the worker container and acts as the interface
to the container instance.

.. code-block:: python

    class DjangoWorkerContainer(CeleryWorkerContainer):
        @property
        def client(self) -> Any:
            return self

        @classmethod
        def version(cls) -> str:
            return celery.__version__

        @classmethod
        def log_level(cls) -> str:
            return "INFO"

        @classmethod
        def worker_name(cls) -> str:
            return "django_tests_worker"

        @classmethod
        def worker_queue(cls) -> str:
            return "celery"

Next, we build our worker image using the `build <https://github.com/Jc2k/pytest-docker-tools?tab=readme-ov-file#images>`_
and `container <https://github.com/Jc2k/pytest-docker-tools?tab=readme-ov-file#containers>`_ fixtures.

.. code-block:: python

    worker_image = build(
        path=".",
        dockerfile="tests/DjangoWorker.Dockerfile",
        tag="pytest-celery/examples/django:example",
        buildargs=DjangoWorkerContainer.buildargs(),
    )


    default_worker_container = container(
        image="{worker_image.id}",
        ports=fxtr("default_worker_ports"),
        environment=fxtr("default_worker_env"),
        network="{default_pytest_celery_network.name}",
        volumes={
            "{default_worker_volume.name}": defaults.DEFAULT_WORKER_VOLUME,
            os.path.abspath(os.getcwd()): {
                "bind": "/src",
                "mode": "rw",
            },
        },
        wrapper_class=DjangoWorkerContainer,
        timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
    )

In this case, we also mount the project directory to ``/src`` in the container, so that we can install the project
inside the container and access the Django project files.

Lastly, we override the default worker container class with our custom class.

.. note::
    This is only required when overriding the default worker.

.. code-block:: python

    @pytest.fixture
    def default_worker_container_cls() -> type[CeleryWorkerContainer]:
        return DjangoWorkerContainer


    @pytest.fixture(scope="session")
    def default_worker_container_session_cls() -> type[CeleryWorkerContainer]:
        return DjangoWorkerContainer

test_tasks.py
~~~~~~~~~~~~~

The ``test_tasks.py`` file contains the tests for the ``demoapp`` tasks.
It can directly import the tasks and the :func:`celery_setup <pytest_celery.fixtures.setup.celery_setup>` will
run the django app worker so the tasks can be tested.

.. code-block:: python

    from demoapp.tasks import add
    from demoapp.tasks import count_widgets


    def test_add(celery_setup):
        assert add.s(1, 2).delay().get() == 3


    def test_count_widgets(celery_setup):
        assert count_widgets.s().delay().get() == 0

.. note::
    Don't forget to ``export DJANGO_SETTINGS_MODULE=proj.settings`` and run migration
    when running the example locally.

    See `CI <https://github.com/celery/pytest-celery/blob/main/.github/workflows/examples.yml>`_ for a usage example.
