.. _resources:

==================
 Useful Resources
==================

:Release: |version|
:Date: |today|

This section contains additional resources that may be useful when developing tests with :pypi:`pytest <pytest>`,
:pypi:`pytest-celery <pytest-celery>`, and general :pypi:`celery <celery>` related testing articles, guides and tutorials.

**You're welcome to contribute to this list!**

.. contents::
    :local:
    :depth: 2

Other Plugins
~~~~~~~~~~~~~

- :pypi:`pytest-rerunfailures <pytest-rerunfailures>`: Do to the natural sensitivity of simulating Celery environments over Docker, it's
  common to have flaky tests due to failing docker resources. This plugin provide useful features to rerun failed tests, skipping tests that
  failed due to actual assertion errors.
