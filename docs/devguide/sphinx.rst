.. _sphinx:

======================
 Shpinx Documentation
======================

:Release: |version|
:Date: |today|

The plugin uses the :pypi:`sphinx_celery <sphinx_celery>` engine to generate the documentation.
The documentation is written in reStructuredText format and is located in the ``docs`` directory of the repository.

.. contents::
    :local:
    :depth: 2

Building the documentation
==========================

To build the documentation, use the :ref:`tox_docs` tox environment.

Live Documentation
==================

To serve the documentation locally, use the :ref:`tox_docs-livehtml` tox environment.

Generate API Documentation
==========================

To generate the API documentation, use the :ref:`tox_docs-apidoc` tox environment.

Linting the documentation
=========================

To lint the documentation, use the :ref:`tox_lint` tox environment, or these Makefile commands::

    make -C ./docs apicheck
    make -C ./docs linkcheck
    make -C ./docs configcheck

Makefile
========

The docs are managed using the following Makefile:

.. literalinclude:: ../../docs/Makefile
    :language: make
    :caption: docs.Makefile
    :start-after: .PHONY: help
    :end-before: .PHONY: clean
