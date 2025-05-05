===================================
 Official pytest plugin for Celery
===================================

Welcome to :pypi:`pytest-celery <pytest-celery>`, the official pytest plugin for Celery.

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

.. _`BSD License`: https://www.opensource.org/license/BSD-3-Clause

.. image:: https://opencollective.com/static/images/opencollectivelogo-footer-n.svg
   :target: https://opencollective.com/celery
   :alt: Open Collective logo
   :width: 240px

`Open Collective <https://opencollective.com/celery>`_ is our community-powered funding platform that fuels Celery's
ongoing development. Your sponsorship directly supports improvements, maintenance, and innovative features that keep
Celery robust and reliable.

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
