.. _release:

==============================
 How to release a new version
==============================

:Release: |version|
:Date: |today|

The following guide will describe the steps to release a new version of the :pypi:`pytest-celery <pytest-celery>` plugin.
It will explain how does the CI/CD pipeline work and how to trigger a new release.

.. contents::
    :local:
    :depth: 2

CI/CD Pipeline
==============

Continuous Integration
~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 1.0.0

The `CI <https://github.com/celery/pytest-celery/actions>`_ platform is based on GitHub Actions and it is triggered on every push to the repository,
and on every pull request, according to the changes made.

The configuration files for the CI pipeline are located in the `.github/workflows <https://github.com/celery/pytest-celery/tree/main/.github/workflows>`_
directory of the repository.

CI Tests
--------

Unit, Integration and Smoke tests.

.. literalinclude:: ../../.github/workflows/python-package.yml
    :language: yaml
    :caption: .github/workflows/python-package.yml

Parallel Tests
--------------

These are the :ref:`tox_parallel` and :ref:`tox_xdist` tox environments. The purpose
of this CI pipeline is to make sure that the plugin is compatible with parallel running, both
in terms of supporting :pypi:`pytest-xdist <pytest-xdist>` and functionally (i.e. that the plugin
does not break when running in parallel).

.. literalinclude:: ../../.github/workflows/parallel-support.yml
    :language: yaml
    :caption: .github/workflows/python-package.yml

Linting
-------

Standard linting checks.

.. literalinclude:: ../../.github/workflows/linter.yml
    :language: yaml
    :caption: .github/workflows/linting.yml

Examples
--------

The official plugin examples are tested as part of the standard CI pipeline.

.. literalinclude:: ../../.github/workflows/examples.yml
    :language: yaml
    :caption: .github/workflows/examples.yml

Docker
------

This pipeline is used to to make sure the provided Dockerfiles from the plugin are built successfully.

.. literalinclude:: ../../.github/workflows/docker.yml
    :language: yaml
    :caption: .github/workflows/docker.yml

.. _continuous_deployment:

Continuous Deployment
~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 1.0.0

The `CD <https://github.com/celery/pytest-celery/actions/workflows/deploy.yml>`_ is configured to deploy a new
release to the `PyPI <https://pypi.org/project/pytest-celery/#history>`_ package index.

The following release workflow is triggered automatically when a new released is tagged and published on GitHub.

.. literalinclude:: ../../.github/workflows/deploy.yml
    :language: yaml
    :caption: .github/workflows/deploy.yml

.. note::

    The ``poetry version`` command should say there's nothing to change, because this should have been done in the PR that prepared the release.

Release Steps
=============

1. Celery Tests
~~~~~~~~~~~~~~~

The plugin is used as the official testing infrastructure for Celery. Every new release
requires manually testing that the new version works as expected with the Celery test suite.

To run the Celery test suite with the new version of the plugin, modify the Celery test environment as follows:

`test.txt <https://github.com/celery/celery/blob/main/requirements/test.txt#>`_
-------------------------------------------------------------------------------

Comment out the pytest-celery `installation line <https://github.com/celery/celery/blob/main/requirements/test.txt#L2>`_.

`tox.ini <https://github.com/celery/celery/blob/main/tox.ini>`_
---------------------------------------------------------------

Add ``-e "../pytest-celery[all]"`` to the `deps <https://github.com/celery/celery/blob/main/tox.ini#L30>`_ list.

.. code-block:: ini

    [testenv]
    ...
    deps=
        -e "../pytest-celery[all]"
        -r{toxinidir}/requirements/test.txt
    ...

And then execute with tox::

    tox -e 3.12-smoke -- -n auto

This will run the Celery test suite with the new version of the plugin in edit mode, allowing
you to test the new version before releasing it and tweaking it if necessary to debug any issues.

.. tip::

    Use the following snippet to run all of the tests with the new version of the plugin:

    Pull RabbitMQ & Redis images for the integration tests:

    .. code-block:: console

        docker run -d -p 6379:6379 --name redis redis:latest
        docker run -d -p 5672:5672 -p 15672:15672 --name rabbitmq rabbitmq:management

    Unit Tests:

    .. code-block:: console

        tox -e 3.12-unit

    Integration Tests:

    .. code-block:: console

        docker start rabbitmq redis
        tox -e 3.12-integration-rabbitmq_redis
        docker stop rabbitmq redis

    Unit & Integration & Smoke Tests:

    .. code-block:: console

        tox -e 3.12-unit && docker start rabbitmq redis && tox -e 3.12-integration-rabbitmq_redis && docker stop rabbitmq redis && tox -e 3.12-smoke -- -n auto

.. warning::

    The instructions above assume you have the :pypi:`pytest-celery <pytest-celery>` and :pypi:`celery <celery>` repositories
    cloned in the same root directory.

2. Release PR
~~~~~~~~~~~~~

To make a new release, you need to create a new PR with one of these titles.

- **Official Release**: Prepare for release: vX.Y.Z
- **Pre-release**: Prepare for (pre) release: vX.Y.Z

The PR should contain the following changes:

- Version bump using `poetry version <https://python-poetry.org/docs/cli#version>`_ command.
- Changelog update.

This PR will be used as a double check for the CI to make sure everything passes successfully before releasing the new version.
Once this PR is merged, the last step is to `release a version on GitHub <https://github.com/celery/pytest-celery/releases/new>`_.
This will trigger the :ref:`CD pipeline <continuous_deployment>` to deploy the new release to PyPI automatically.

SemVer
------

If you're not sure how to number the version, consult the `SemVer <https://semver.org/>`_ documentation.

3. Post-release
~~~~~~~~~~~~~~~

After the release is done, you should update the official Celery to use the new version of the plugin, in the
same `test.txt <https://github.com/celery/celery/blob/main/requirements/test.txt#>`_ that you modified earlier.

Future Releases
===============

Releases should be planned in the official `Milestones <https://github.com/celery/pytest-celery/milestones>`_ of the repository.
Each milestone should include in its description what is planned for the release and when is the expected release date.
