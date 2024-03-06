.. _advanced-installation:

=============================
 Advanced Installation Guide
=============================

:Release: |version|
:Date: |today|

The pytest-celery plugin uses the environment dependencies to install and configure the default :ref:`setup-matrix`.
The available dependencies are the feature flags for the available :ref:`vendors`.

This guide will explain how to install the plugin, how to use the dependencies feature flags and how to
fit the configurations to your needs.

We will start by reviewing the standard installation instructions.

.. contents::
    :local:
    :depth: 2

.. include:: ../includes/installation.txt

.. _advanced-installation-section:

Advanced Installation
=====================

.. versionadded:: 1.0.0

In this section, we'll improve our understanding of the plugin installation process and how to customize it.

Feature Flags
~~~~~~~~~~~~~

The installed dependencies dynamically configure which vendors are available for the plugin to use.
Each vendor will provide its set of components, such as the broker, backend, and the worker, and the plugin will
automatically add the matching components to the default setup matrix.

For example, let's assume you want to use the RabbitMQ/Redis combination.

1. For RabbitMQ we will need :pypi:`kombu`.
2. For Redis we will need :pypi:`redis`.

To install the plugin with the RabbitMQ/Redis combination, you will need to install the following dependencies:

.. code-block:: bash

    pip install "pytest-celery[redis]"

Let's break down the command:

- The ``pytest-celery`` is the plugin package, it will install the plugin alongside Celery and its dependencies,including **Kombu** (if not installed already).
- The ``[redis]`` is the feature flag for the Redis vendor, it will install the :pypi:`redis` package and configure the plugin to use it which will add the Redis backend and Redis broker components to the default setup matrix.

Experimental Vendors
~~~~~~~~~~~~~~~~~~~~

:ref:`vendors` that are in not stable, will not be added to the default setup matrix.
To use the experimental vendors, you will need to configure the setup matrix manually.

.. tip::

    The automatic vendors detection is implemented in :mod:`defaults.py <pytest_celery.defaults>`.

The ``all`` Extra
~~~~~~~~~~~~~~~~~

The ``all`` extra is a special feature flag that will install all available vendors and their dependencies.

.. code-block:: bash

    pip install "pytest-celery[all]"

This command will install the plugin and configure it to use all available **stable** vendors in a setup matrix for each test case
that uses the :ref:`test-setup`.

.. warning::

    The ``all`` extra will install **all** of the vendors dependencies, including the experimental vendor's dependencies,
    to allow manual configuration of the setup matrix.
