===================================================
 Pytest Celery - Official pytest plugin for Celery
===================================================

Welcome to pytest-celery, the official pytest plugin for Celery.

The pytest-celery plugin introduces significant enhancements with the introduction of
version >= 1.0.0, shifting towards a Docker-based approach for smoke and production-like testing.
While the `celery.contrib.pytest` API continues to support detailed integration
and unit testing, the new Docker-based methodology is tailored for testing in 
environments that closely mirror production settings.

Adopting version >= 1.0.0 enriches your testing suite with these new capabilities
without affecting your existing tests, allowing for a smooth upgrade path.
The documentation here will navigate you through utilizing the Docker-based approach.
For information on the `celery.contrib.pytest` API for integration and unit testing,
please refer to the `official documentation`_.

.. _`official documentation`: https://docs.celeryproject.org/en/latest/userguide/testing.html

The pytest-celery plugin is Open Source and licensed under the `BSD License`_.

.. _`BSD License`: http://www.opensource.org/licenses/BSD-3-Clause

Donations
=========

This project relies on your generous donations.

If you are using Pytest Celery to test a commercial product, please consider becoming
our `backer`_ or our `sponsor`_ to ensure Pytest Celery's future.

.. _`backer`: https://opencollective.com/celery
.. _`sponsor`: https://opencollective.com/celery

Getting Started
===============

- If you're new to pytest-celery you can get started by following the :ref:`getting-started` tutorial.
- You can also check out the :ref:`FAQ <faq>`.

Contents
========

.. toctree::
    :maxdepth: 1

    copyright

.. toctree::
    :maxdepth: 2

    getting-started/index
    userguide/index
    devguide/index

.. toctree::
    :maxdepth: 1

    reference/index
    contributing
    faq
    changelog
    glossary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
