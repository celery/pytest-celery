.. _app-conf:

================================
 Prepare the Celery Application
================================

:Release: |version|
:Date: |today|

The plugin is designed to allow preparing a Celery_ app object that will be applied
to the worker container for each test case. It is useful for configuring the worker
using the standard Celery_ API and uses the pytest fixtures mechanism to allow controlling
the worker configuration pipeline.

This guide will teach you how to utilize this mechanism to control the worker configuration
for your test cases.

.. _Celery: https://docs.celeryq.dev/en/stable/reference/celery.html#celery.Celery

.. contents::
    :local:
    :depth: 2

.. include:: ../includes/worker-breakdown.txt

Worker App Configuration
========================

.. versionadded:: 1.0.0

To configure the worker app, use the :func:`default_worker_app <pytest_celery.vendors.worker.fixtures.default_worker_app>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_app(default_worker_app: Celery) -> Celery:
        app = default_worker_app
        # configure the app here
        return app

Modular Configuration
~~~~~~~~~~~~~~~~~~~~~

The worker app instance can be configured differently for each test case using the
`Fixture availability <https://docs.pytest.org/en/latest/reference/fixtures.html#fixture-availability>`_ feature of pytest.

For example,

.. code-block:: python

    @pytest.fixture
    def default_worker_app(default_worker_app: Celery) -> Celery:
        app = default_worker_app
        app.conf.A = X
        return app


    class test_example:
        @pytest.fixture
        def default_worker_app(self, default_worker_app: Celery) -> Celery:
            app = default_worker_app
            # app.conf.A is already set to X
            app.conf.B = Y
            return app

        def test_worker_app(self, celery_setup: CeleryTestSetup):
            assert celery_setup.app.conf.A == X
            assert celery_setup.app.conf.B == Y

.. warning::

    The ``default_worker_app`` fixture is called before the worker container
    is created so using it in a test case will not change the worker's initialization
    pipeline as it is already completed by the time the test case is executed.
