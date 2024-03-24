.. _tox:

==================
 Tox Environments
==================

:Release: |version|
:Date: |today|

:pypi:`Tox <tox>` is used to manage the development environments, which are defined in the ``tox.ini`` file.

To see all possible environments, run::

    tox -av

This guide will explain the different environments and how they are used.

.. contents::
    :local:
    :depth: 1

tox
===

There are three test environments:

- **unit**: Run the unit tests. Does not require docker.
- **integration**: Run the integration tests. Requires docker.
- **smoke**: Run the smoke tests. Requires docker. Simulates a production environment for the plugin.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [tox]
    :end-before: [gh-actions]

Execution
~~~~~~~~~

To run the tests, use::

    tox -e py3<version>-<env>

Where ``<version>`` is the python version and ``<env>`` is the environment to run.

For example,

- To run the unit tests with python 3.12, use::

    tox -e py312-unit

- To run the integration tests with python 3.12, use::

    tox -e py312-integration

- To run the smoke tests with python 3.12, use::

    tox -e py312-smoke

gh-actions
==========

This section refers to the GitHub Actions configuration with :pypi:`tox-gh-actions <tox-gh-actions>`.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [gh-actions]
    :end-before: [testenv]

testenv
=======

These configurations are used to define the base settings for the tox environments.

.. note::

    The convention is to use the latest python version as the default.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv]
    :end-before: [testenv:xdist]

.. _tox_xdist:

xdist
=====

This environment is used to run **all** the tests in parallel using :pypi:`pytest-xdist <pytest-xdist>`.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv:xdist]
    :end-before: [testenv:parallel]

Execution
~~~~~~~~~

To run this environment, use::

    tox -e xdist

.. _tox_parallel:

parallel
========

This environment is used to run the tests in parallel using both :pypi:`tox <tox>` and :pypi:`pytest-xdist <pytest-xdist>`.
It will run the test environments in parallel using the ``-p auto`` option from tox, and then run each environment itself in
parallel using pytest-xdist with the ``-n auto`` option.

It is slightly more efficient than the :ref:`tox_xdist` tox environment, but less stable due to high resource usage.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv:parallel]
    :end-before: [testenv:mypy]

Execution
~~~~~~~~~

To run this environment, use::

    tox -e parallel

mypy
====

Standard mypy linting.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv:mypy]
    :end-before: [testenv:lint]

Execution
~~~~~~~~~

To run this environment, use::

    tox -e mypy

.. _tox_lint:

lint
====

Standard linting including doc linting.

.. note::

    Does not include mypy linting.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv:lint]
    :end-before: [testenv:clean]

Execution
~~~~~~~~~

To run this environment, use::

    tox -e lint

To run **just the pre-commit** locally (without tox, without doc), use::

    pre-commit run --show-diff-on-failure --color=always --all-files

.. _tox_clean:

clean
=====

Cleans the environment from artifacts and temporary files.

.. tip::

    Very useful for cleaning up docker artifacts when stopping tests in the middle of execution.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv:clean]
    :end-before: [testenv:docs]

Execution
~~~~~~~~~

To run this environment, use::

    tox -e clean

.. _tox_docs:

docs
====

Builds the documentation.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv:docs]
    :end-before: [testenv:docs-livehtml]

Execution
~~~~~~~~~

To run this environment, use::

    tox -e docs

.. _tox_docs-livehtml:

docs-livehtml
=============

Builds the documentation and serves it locally at http://0.0.0.0:7010/

Supports hot-reloading.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv:docs-livehtml]
    :end-before: [testenv:docs-apidoc]

Execution
~~~~~~~~~

To run this environment, use::

    tox -e docs-livehtml

.. _tox_docs-apidoc:

docs-apidoc
===========

Generates the :ref:`apiref`.

.. tip::

    If you added a new file to the plugin's source code, you need to run this environment to update the documentation.
    It will find the new files and add them to the documentation automatically.

.. note::

    This environment is idempotent and will result in the same output if run multiple times.

.. literalinclude:: ../../tox.ini
    :language: ini
    :caption: tox.ini
    :start-after: [testenv:docs-apidoc]

Execution
~~~~~~~~~

To run this environment, use::

    tox -e docs-apidoc
