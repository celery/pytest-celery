
|build-status| |coverage| |license| |semgrep| |pyversion| |pyimp| |ocbackerbadge| |ocsponsorbadge| |poetry|

:Version: 1.0.0rc4
:Web: https://pytest-celery.readthedocs.io/en/latest/
:Download: https://pypi.org/project/pytest-celery/
:Source: https://github.com/celery/pytest-celery/

===================================
 Official pytest plugin for Celery
===================================

Welcome to `pytest-celery`_, the official pytest plugin for Celery.

.. _`pytest-celery`: https://pypi.org/project/pytest-celery/

The pytest-celery plugin introduces significant enhancements with the introduction of
version >= 1.0.0, shifting towards a Docker-based approach for smoke and production-like testing.
While the ``celery.contrib.pytest`` API continues to support detailed integration
and unit testing, the new Docker-based methodology is tailored for testing in
environments that closely mirror production settings.

Adopting version >= 1.0.0 enriches your testing suite with these new capabilities
without affecting your existing tests, allowing for a smooth upgrade path.
The documentation here will navigate you through utilizing the Docker-based approach.
For information on the ``celery.contrib.pytest`` API for integration and unit testing,
please refer to the `official documentation`_.

.. _`official documentation`: https://docs.celeryproject.org/en/latest/userguide/testing.html

The pytest-celery plugin is Open Source and licensed under the `BSD License`_.

.. _`BSD License`: http://www.opensource.org/licenses/BSD-3-Clause

Donations
=========

This project relies on your generous donations.

If you are using pytest-celery to test a commercial product, please consider becoming
our `backer`_ or our `sponsor`_ to ensure pytest-celery's future.

.. _`backer`: https://opencollective.com/celery
.. _`sponsor`: https://opencollective.com/celery

Getting Started
===============

- If you're new to pytest-celery you can get started by following the `Getting Started`_ tutorial.
- You can also check out the `FAQ`_.

.. _`Getting Started`: https://docs.celeryq.dev/projects/pytest-celery/en/latest/getting-started/index.html#getting-started
.. _`FAQ`: https://docs.celeryq.dev/projects/pytest-celery/en/latest/faq.html#faq

Contents
========

- `Copyright <https://docs.celeryq.dev/projects/pytest-celery/en/latest/copyright.html>`_

- `Getting Started <https://docs.celeryq.dev/projects/pytest-celery/en/latest/getting-started/index.html>`_
    - `Introduction to pytest-celery <https://docs.celeryq.dev/projects/pytest-celery/en/latest/getting-started/introduction.html>`_
    - `First Steps with pytest-celery <https://docs.celeryq.dev/projects/pytest-celery/en/latest/getting-started/first-steps.html>`_
    - `Next Steps <https://docs.celeryq.dev/projects/pytest-celery/en/latest/getting-started/next-steps.html>`_
    - `Vendors <https://docs.celeryq.dev/projects/pytest-celery/en/latest/getting-started/vendors.html>`_
    - `Help <https://docs.celeryq.dev/projects/pytest-celery/en/latest/getting-started/help.html>`_

- `User Guide <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/index.html>`_
    - `Advanced Installation Guide <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/advanced-installation.html>`_
    - `Test Setup Matrix <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/setup-matrix.html>`_
    - `How to prepare the Celery application <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/app-conf.html>`_
    - `How to inject your own utility functions <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/utils-module.html>`_
    - `How to add tasks <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/tasks.html>`_
    - `Built-in Tasks <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/default-tasks.html>`_
    - `How to connect signal handlers <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/signals.html>`_
    - `Standalone Celery Bug Report <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/celery-bug-report.html>`_
    - `Examples <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/examples/index.html>`_
    - `Useful Resources <https://docs.celeryq.dev/projects/pytest-celery/en/latest/userguide/resources/index.html>`_

- `Plugin Development Guide <https://docs.celeryq.dev/projects/pytest-celery/en/latest/devguide/index.html>`_
    - `Local Development Environment <https://docs.celeryq.dev/projects/pytest-celery/en/latest/devguide/local-development-environment.html>`_
    - `Tox Environments <https://docs.celeryq.dev/projects/pytest-celery/en/latest/devguide/tox.html>`_
    - `Sphinx Documentation <https://docs.celeryq.dev/projects/pytest-celery/en/latest/devguide/sphinx.html>`_
    - `How to release a new version <https://docs.celeryq.dev/projects/pytest-celery/en/latest/devguide/release.html>`_

- `API Documentation <https://docs.celeryq.dev/projects/pytest-celery/en/latest/reference/index.html>`_
- `Contributing <https://docs.celeryq.dev/projects/pytest-celery/en/latest/contributing.html>`_
- `FAQ <https://docs.celeryq.dev/projects/pytest-celery/en/latest/faq.html>`_
- `Change history <https://docs.celeryq.dev/projects/pytest-celery/en/latest/changelog.html>`_
- `Glossary <https://docs.celeryq.dev/projects/pytest-celery/en/latest/glossary.html>`_

.. |build-status| image:: https://github.com/celery/pytest-celery/actions/workflows/python-package.yml/badge.svg
    :alt: Build status
    :target: https://github.com/celery/pytest-celery/actions/workflows/python-package.yml

.. |coverage| image:: https://codecov.io/github/celery/pytest-celery/coverage.svg?branch=main
    :target: https://codecov.io/github/celery/pytest-celery?branch=main

.. |license| image:: https://img.shields.io/pypi/l/pytest-celery.svg
    :alt: BSD License
    :target: https://opensource.org/licenses/BSD-3-Clause

.. |semgrep| image:: https://img.shields.io/badge/semgrep-security-green.svg
    :alt: Semgrep security
    :target: https://go.semgrep.dev/home

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/pytest-celery.svg
    :alt: Supported Python versions.
    :target: https://pypi.org/project/pytest-celery/

.. |pyimp| image:: https://img.shields.io/pypi/implementation/pytest-celery.svg
    :alt: Supported Python implementations.
    :target: https://pypi.org/project/pytest-celery/

.. |ocbackerbadge| image:: https://opencollective.com/celery/backers/badge.svg
    :alt: Backers on Open Collective
    :target: #backers

.. |ocsponsorbadge| image:: https://opencollective.com/celery/sponsors/badge.svg
    :alt: Sponsors on Open Collective
    :target: #sponsors

.. |poetry| image:: https://img.shields.io/badge/poetry-yes-blue.svg
    :alt: Poetry
    :target: https://python-poetry.org/
