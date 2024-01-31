.. _getting-started_intro:

===============================
 Introduction to Pytest Celery
===============================

.. contents::
    :local:
    :depth: 1

What is Pytest Celery?
======================

It is an essential pytest_ plugin designed for Celery application developers.
It enables dynamic orchestration of Celery environments for testing tasks in isolated conditions,
leveraging Docker_ & pytest-docker-tools_ for environment simulation.

The plugin is designed to be highly configurable, and can be used to test a wide range of Celery architectures.
It encapsulate the complexity of setting up a Celery environment, and provides a simple interface to access
the Celery architecture components in a test case.

The plugin functions as the backbone of Celery's testing infrastructure, and is used to test Celery itself.
The pytest-celery plugin is considered the official Celery testing infrastructure, internally and externally.

.. _pytest: https://docs.pytest.org
.. _Docker: https://www.docker.com
.. _pytest-docker-tools: https://pypi.org/project/pytest-docker-tools/

What do I need?
===============

.. sidebar:: Version Requirements
    :subtitle: Pytest Celery version 1.0 runs on

    - Python ❨3.8, 3.9, 3.10, 3.11, 3.12❩

    Celery is required and may be installed separately or automatically using the `celery` extra.
    When used with the `celery` extra, pytest-celery will install the latest version of Celery
    and a predefined set of extras.

    Pytest Celery is Celery-agnostic, and should work with virtually any version of Celery.

    .. note:: Currently, due to limited resources, we are unable to officially support Microsoft Windows.
        Please don't open any issues related to that platform.

The pytest-celery plugin is using docker containers to define a Celery setup for a test. This means
the testing environment must have a working Docker installation. The plugin provides built-in containers,
but it is expected to be configured with the architecture and requirements of the target project.

Get Started
===========

Sometimes jumping into the deep water is the best way to learn how to swim.
A good place to start is the `examples`_ directory. It contains a few examples that demonstrate
the capabilities of the plugin.

Other useful use cases are the `smoke-tests`_ directory of the Celery repository.
The Celery smoke tests are the official production environment for pytest-celery, and may be
insightful for understanding how to use the plugin from a production perspective.

Essential Resources
~~~~~~~~~~~~~~~~~~~

The pytest-celery plugin is using core pytest features to encapsulate the complexity of setting up a Celery environment
into a simple interface. It is highly recommended to familiarize yourself with the following resources to get the most out of the plugin.

- `Fixtures reference`_: Detailed guide to pytest fixtures. **Extremely** useful for understanding how to use the plugin effectively.
- `Pytest parametrization`_: Guide for pytest parametrization. Useful for understanding how the Celery architecture is generated.

.. _examples: https://github.com/celery/pytest-celery/tree/main/examples
.. _smoke-tests: https://github.com/celery/celery/tree/main/t/smoke
.. _Fixtures reference: https://docs.pytest.org/en/latest/reference/fixtures.html#fixtures
.. _Pytest parametrization: https://docs.pytest.org/en/latest/how-to/parametrize.html

Additional resources can be found in the :ref:`getting-started_resources` section.

Pytest Celery is…
=================

.. topic:: \

    - **Simple**

        The plugin provides a single entry point to the test case and makes sure
        everything is configured according to the selected architecture and requirements.

        By default, all of the supported architecture components are added to a matrix of all possible combinations.
        Pytest will generate a test case for each combination, and will run it in an isolated environment.

        This allows separation of concerns, and makes it simple to access different architectures in a single test case,
        for example:

        .. code-block:: python

            def test_hello_world(celery_setup):
                assert celery_setup.ready()

        This code will generate test cases for all possible combinations of the supported brokers and backends, using the latest
        version of Celery. Under the context of the test, each combination will be available as a `celery_setup` fixture,
        with access to all of the required components, and will run in an isolated environment.

    - **Flexible**

        The plugin is highly configurable, and can be used to test a wide range of Celery architectures.
        It can be configured to use a specific version of Celery, or to use a specific version of a broker or backend.
        It can also be configured to use a custom broker or backend, or to use a custom Celery application.

        For basic usage, the plugin provides default components that can be configured and extended.

        For more advanced use cases, the plugin uses the pytest fixtures mechanism to allow injecting
        custom components into the environment and build a custom Celery architecture for your project.

        For example, see the `rabbitmq_management`_ example, which demonstrates how to replace the default
        broker matrix with a single RabbitMQ Management broker.

        .. _rabbitmq_management: https://github.com/celery/pytest-celery/tree/main/examples/rabbitmq_management

    - **Fast**

        The plugin is designed to run tests in parallel using isolated environments. It supports the pytest-xdist_ plugin
        to run tests in parallel, and scales well with available resources to improve the overall test suite performance.

        .. _pytest-xdist: https://pypi.org/project/pytest-xdist/

    - **Annotated**

        The codebase is fully annotated with type hints, and is tested with mypy_ to ensure type safety accros the board,
        allowing a better development experience.

        .. _mypy: https://mypy.readthedocs.io

.. topic:: It supports

    .. hlist::
        :columns: 2

        - **Workers**

            - Latest Celery version.
            - Custom worker.

        - **Brokers**

            - RabbitMQ.
            - Redis.
            - Custom broker.

        - **Backends**

            - Redis.
            - Memcached.
            - Custom backend.

        - **Clusters**

            - Worker clusters.
            - Broker clusters.
            - Backend clusters.

Features
========

.. topic:: \

    .. hlist::
        :columns: 2

        - **Architecture Injection**

            By default, a set of predefined components is used to build the Celery architecture for each test.
            Each built-in component can be either configured or replaced with a custom replacement.

            Architecture injection can be done at different layers, and can be used to
            replace only specific elements of the architecture pipeline, or to replace the entire pipeline altogether.

        - **Docker Based**

            The plugin uses docker containers to build the Celery architecture for each test.
            This means that the plugin is not limited to a specific versions, and can be used to test
            potentially any Celery setup.

        - **Batteries Included**

            The plugin provides a set of built-in components that can be used to test ideas quickly.
            You can start with the default settings, and gradually modify the configrations to fine tune
            the test environment. By focusing on the test case, you can quickly iterate and test ideas,
            without wasting time on the overhead of setting up different environment manually.

        - **Code Generation**

            One of the challenges in testing production Celery applications is the need to inject testing infrastructure
            into the Celery worker container at runtime. The plugin provides a code generation mechanism that can be used
            to inject code into the Celery worker container at runtime according to the test case. This opens the door to
            a wide range of testing scenarios, and allows higher level of control over the tested Celery application.

        - **Isolated Environments**

            Each test case is executed in an isolated environment. This means that each test case has its own Celery architecture,
            and is not affected by other test cases. Tests may run in parallel and take care of tearing down themselves when they
            are done, regardless of the test result.

        - **CI/CD Friendly**

            The plugin is designed to match local test runs with CI/CD test runs to ensure consistent results
            across different environments and support extended configuration options for each environment.
            It uses tox_ to manage the test environments, and provides a set of predefined environments that
            can be used to test the plugin in different configurations.

            Run `tox -av` to see the list of available environments.

            .. _tox: https://tox.readthedocs.io

        - **Tests as first class citizens**

            The plugin is designed to enhance testing capabilities by treating tests as first class citizens.
            It's based on `S.O.L.I.D`_ principles and provides APIs for developing high quality tests suites.

            .. _S.O.L.I.D: https://en.wikipedia.org/wiki/SOLID

Quick Jump
==========

.. topic:: I want to ⟶

    .. hlist::
        :columns: 2

        - :ref:`To read Contributing <contributing>`
        - :ref:`To read FAQ <faq>`
        - :ref:`To read API Reference <apiref>`

.. topic:: Jump to ⟶

    .. hlist::
        :columns: 4

        - :ref:`Contributing <contributing>`
        - :ref:`FAQ <faq>`
        - :ref:`API Reference <apiref>`

.. include:: ../includes/installation.txt
