.. _intro:

===============================
 Introduction to Pytest Celery
===============================

.. contents::
    :local:
    :depth: 1

What's a Pytest Plugin?
=======================

TBD

What do I need?
===============

.. sidebar:: Version Requirements
    :subtitle: Pytest Celery version 1.0 runs on

    - Python ❨3.8, 3.9, 3.10, 3.11, 3.12❩

    Latest celery version comes out of the box but it is recommended to use your own version.

    Pytest Celery is a project with minimal funding,
    so we don't support Microsoft Windows.
    Please don't open any issues related to that platform.

TBD

TODO: Comment about pytest-docker-tools dependency

Get Started
===========

Until the documentation is ready, you can check the following locations
for useful information (in order of usefulness):

- CI_ configuration files.
- Examples_ directory.
- Tests_ directory.
- Source_ code.

.. _CI: https://github.com/celery/pytest-celery/tree/main/.github/workflows
.. _Examples: https://github.com/celery/pytest-celery/tree/main/examples
.. _Tests: https://github.com/celery/pytest-celery/tree/main/tests
.. _Source: https://github.com/celery/pytest-celery/tree/main/src/pytest_celery

Pytest Celery is…
=================

.. topic:: \

    - **Simple**

        See example below:

        .. code-block:: python

            def test_hello_world(celery_setup):
                assert celery_setup.ready()

    - **In development**

        As you can see, the documentation is under construction.


.. topic:: It supports

    .. hlist::
        :columns: 2

        - **Cool Stuff**

            - Highlights.
            - More highlights.

        - **Celery Stuff**

            - Testing infra capabilities.

Features
========

.. topic:: \

    .. hlist::
        :columns: 2

        - **Pytest**

            This is a pytest plugin.

            :ref:`Read more… <faq>`.

        - **Celery**

            For Celery.

            :ref:`Read more… <faq>`.

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
