.. _faq:

============================
 Frequently Asked Questions
============================

.. contents::
    :local:

Getting Started
===============

What are the prerequisites for installing pytest-celery?
--------------------------------------------------------

**Answer:** The celery package and the required dependencies for the used :ref:`vendors`.

How do I install pytest-celery?
-------------------------------

**Answer:** See :ref:`installation`.

What initial configuration is required to start using pytest-celery?
--------------------------------------------------------------------

**Answer:** Generally speaking, everything is set up by default. However, you may need to tweak
some settings to fit your specific use case.

For new projects, it is recommended to at least start with a ``pytest.ini`` file at the root of your project
with the following content:

.. code-block:: ini

    [pytest]
    log_cli = true
    log_cli_level = INFO
    log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
    log_cli_date_format = %Y-%m-%d %H:%M:%S

This will enable plugin logging to the console, which can be helpful for debugging.

Are there any example projects or templates to help me get started?
-------------------------------------------------------------------

**Answer:** Yes. See the :ref:`examples` section.

In addition, you may review the `official Celery smoke tests <https://github.com/celery/celery/tree/main/t/smoke>`_
which are the defacto production environment for the plugin.

Configuration and Customization
===============================

Can I use pytest-celery with different message brokers or backends?
-------------------------------------------------------------------

**Answer:** Yes. The built-in :ref:`vendors` are supported out of the box, but you can also use custom ones,
or reconfigure the built-in ones to fit your needs.

Vendors are different technologies that provides components to the environment.
Such components may be brokers, backends or worker components, which are constructed by a node controller
and a docker container combination.

If you provide your own component (broker/backend/worker) using your own docker image, you may inject
the component into the environment as described in the :ref:`architecture-injection` section.

How can I manage worker concurrency settings in pytest-celery?
--------------------------------------------------------------

**Answer:** Using the :func:`default_worker_app <pytest_celery.vendors.worker.fixtures.default_worker_app>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_app(default_worker_app: Celery) -> Celery:
        app = default_worker_app
        app.conf.worker_concurrency = 42
        return app

For more details, see :ref:`worker-app-configuration`.

How do I simulate different environments using pytest-celery?
-------------------------------------------------------------

**Answer:** See :ref:`manipulating-the-environment`.

Debugging and Troubleshooting
=============================

Why doesn't the worker recognize my tasks?
------------------------------------------

**Answer:** Because you don't use the :func:`default_worker_tasks <pytest_celery.vendors.worker.fixtures.default_worker_tasks>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_tasks(default_worker_tasks: set) -> set:
        from tests import tasks

        default_worker_tasks.add(tasks)
        return default_worker_tasks

For more details, see :ref:`injecting-tasks`.

Why aren't my consumer signal handlers triggering?
--------------------------------------------------

**Answer:** Because you don't use the :func:`default_worker_signals <pytest_celery.vendors.worker.fixtures.default_worker_signals>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_signals(default_worker_signals: set) -> set:
        from tests import signals

        default_worker_signals.add(signals)
        yield default_worker_signals

For more details, see :ref:`injecting-signals-handlers`.

What should I do if the Celery worker doesn't start?
----------------------------------------------------

**Answer:** This is most probably due to docker build failure.

1. Try to build your worker image manually to see if there are any errors. Make sure to use the same arguments as the plugin.
2. If it does, then it is probably due to incorrect setup configuration. Review your fixtures usage.

How can I manually inspect my running setup during a test execution?
--------------------------------------------------------------------

**Answer:** You may place a breakpoint in your test and inspect the environment using any standard tool.

If possible, the `Docker Desktop <https://www.docker.com/products/docker-desktop/>`_ is very helpful for inspecting
the running containers during the test execution.

Integrating with Docker
=======================

How do I get pytest-celery to work with Docker?
-----------------------------------------------

**Answer:** The engine behind the plugin's docker integration is :pypi:`pytest-docker-tools <pytest-docker-tools>`.

It does not interact with Docker directly.

The Docker environment should be install normally, regardless of the plugin.

How can I clean up Docker artifacts left after a test run?
----------------------------------------------------------

**Answer:** You may use this snippet from the :ref:`tox_clean` tox environment.

.. literalinclude:: ../tox.ini
   :language: ini
   :caption: tox.ini
   :start-after: make -C ./docs clean
   :end-before: [testenv:docs]

What are the common pitfalls when integrating pytest-celery with Docker, and how can I avoid them?
--------------------------------------------------------------------------------------------------

**Answer:** The most common issues encountered so far are limited docker resources and network issues.

To avoid these, you may:

1. Increase the resources available to Docker.
2. Use the :pypi:`pytest-rerunfailures <pytest-rerunfailures>` pytest plugin to retry failed tests with:

.. code-block:: console

    --reruns 5 --reruns-delay 60 --rerun-except AssertionError

Experiment with the values to find the best fit for your environment.
