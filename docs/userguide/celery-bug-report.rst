.. _celery-bug-report:

==============================
 Standalone Celery Bug Report
==============================

:Release: |version|
:Date: |today|

The pytest-celery plugin enables the reproduction of Celery bugs through standalone scripts.
These scripts can encapsulate all the required setups and configurations to replicate a potential bug, making it straightforward to share through a new
`bug report issue <https://github.com/celery/celery/issues/new/choose>`_.

This guide will detail the process of creating example bug report scripts using the plugin.

.. contents::
    :local:
    :depth: 2

Disable Setup Matrix
====================

.. versionadded:: 1.0.0

When reporting a bug, you want to have the most simple and specific reproduction environment. To disable the :ref:`setup-matrix`,
you only need to remove the default matrix components from the setup cluster and you do that by either directly disabling the
matching cluster, and/or by setting an exact setup explicitly.

Set Explicit Setup
~~~~~~~~~~~~~~~~~~

Setting the exact components that reproduce the bug is the most efficient method to provide a useful reproduction script. The plugin
is designed in a way that allows you to control the environment outside of the test function, so you can focus the test on the MVP scenario
that reproduces the bug instead of cluttering the test case with preparation code.

Broker
------

Decide **which** broker is needed and set an exact broker to match the environment where the bug was found.

RabbitMQ Broker Snippet
#######################

This will set only the RabbitMQ broker and disable the default broker matrix.

.. code-block:: python

    @pytest.fixture
    def celery_broker_cluster(celery_rabbitmq_broker: RabbitMQTestBroker) -> CeleryBrokerCluster:
        cluster = CeleryBrokerCluster(celery_rabbitmq_broker)
        yield cluster
        cluster.teardown()

To control the version of the RabbitMQ broker, you can use the
:func:`default_rabbitmq_broker_image <pytest_celery.vendors.rabbitmq.fixtures.default_rabbitmq_broker_image>` like this:

.. code-block:: python

    @pytest.fixture
    def default_rabbitmq_broker_image() -> str:
        return "rabbitmq:latest"

To use the ``rabbitmq:management`` label, see the :ref:`examples_rabbitmq-management` example.

Redis Broker Snippet
####################

This will set only the Redis broker and disable the default broker matrix.

.. code-block:: python

    @pytest.fixture
    def celery_broker_cluster(celery_redis_broker: RedisTestBroker) -> CeleryBrokerCluster:
        cluster = CeleryBrokerCluster(celery_redis_broker)
        yield cluster
        cluster.teardown()

To control the version of the Redis broker, you can use the
:func:`default_redis_broker_image <pytest_celery.vendors.redis.broker.fixtures.default_redis_broker_image>` like this:

.. code-block:: python

    @pytest.fixture
    def default_redis_broker_image() -> str:
        return "redis:latest"

Backend
-------

Decide **if a** backend is needed and :ref:`disable the default backend <disable_backend>` if it's not needed or set an exact backend to match
the environment where the bug was found.

Redis Backend Snippet
#####################

This will set only the Redis backend and disable the default backend matrix.

.. code-block:: python

    @pytest.fixture
    def celery_backend_cluster(celery_redis_backend: RedisTestBackend) -> CeleryBackendCluster:
        cluster = CeleryBackendCluster(celery_redis_backend)
        yield cluster
        cluster.teardown()

To control the version of the Redis backend, you can use the
:func:`default_redis_backend_image <pytest_celery.vendors.redis.backend.fixtures.default_redis_backend_image>` like this:

.. code-block:: python

    @pytest.fixture
    def default_redis_backend_image() -> str:
        return "redis:latest"

Memcached Backend Snippet
#########################

This will set only the Memcached backend and disable the default backend matrix.

.. code-block:: python

    @pytest.fixture
    def celery_backend_cluster(celery_memcached_backend: MemcachedTestBackend) -> CeleryBackendCluster:
        cluster = CeleryBackendCluster(celery_memcached_backend)
        yield cluster
        cluster.teardown()

To control the version of the Memcached backend, you can use the
:func:`default_memcached_backend_image <pytest_celery.vendors.memcached.fixtures.default_memcached_backend_image>` like this:

.. code-block:: python

    @pytest.fixture
    def default_memcached_backend_image() -> str:
        return "memcached:latest"

Worker
------

Use the :ref:`built-in-worker` to use a custom version or use the smoke tests's worker to use the source code version.

.. note::

    The Celery smoke tests dev worker is configured to use the source code to install Celery on the worker.
    It is set as the default worker by default in the smoke tests environment.

Built-in Worker Snippet
#######################

This will set the built-in worker to a specific Celery release.

.. code-block:: python

    @pytest.fixture
    def default_worker_celery_version() -> str:
        return "4.4.7"

.. warning::

    The :func:`default_worker_celery_version <pytest_celery.vendors.worker.fixtures.default_worker_celery_version>` is used
    with the ``pip`` install method, so it should be a valid version that can be installed from PyPI.

.. tip::

    Return an empty string to use the latest version.

Smoke Tests Worker Snippet
##########################

To install the worker from source, just run the test script from the `t/smoke/tests <https://github.com/celery/celery/tree/main/t/smoke/tests>`_ directory.

It will automatically set up a `dev <https://github.com/celery/celery/blob/main/t/smoke/workers/dev.py>`_ worker for the test.

Tasks and Signals
-----------------

The plugin provides a :func:`ping task <pytest_celery.vendors.worker.tasks.ping>` by default, but there are other
sources for tasks that can be used to reproduce a scenario.

To use the ping task, import it from the plugin.

.. code-block:: python

    from pytest_celery import ping

The worker will already have it registered by default using the default worker volume.

Adding New Tasks
################

To add new tasks, create a new ``tasks.py`` module and use the :func:`default_worker_tasks <pytest_celery.vendors.worker.fixtures.default_worker_tasks>` fixture
to inject the tasks into the worker as described in the :ref:`injecting-tasks` section.

For example, the tasks module can look like this:

.. code-block:: python

    import celery.utils
    from celery import shared_task


    @shared_task
    def noop(*args, **kwargs) -> None:
        return celery.utils.noop(*args, **kwargs)

And then it can be injected into the worker like this:

.. code-block:: python

    import tasks

    @pytest.fixture
    def default_worker_tasks(default_worker_tasks: set) -> set:
        default_worker_tasks.add(tasks)
        return default_worker_tasks

And be used in a test like this:

.. code-block:: python

    from tasks import noop

    def test_issue_1234(celery_setup: CeleryTestSetup):
        # Running this canvas causes an unexpected exception as described in the bug report...
        assert noop.s().apply_async().get() is None, "The bug causes this assertion to fail..."

Using Celery Tests Tasks
########################

When running the test script from Celery's test suite, the worker already has access to all of the integration
and smoke tests tasks, so you can use them to reproduce a scenario.

All you need to do is to import the tasks from the test suite and use them in the test case.

For example,

.. code-block:: python

    from pytest_celery import CeleryTestSetup

    from t.integration.tasks import identity


    class TestBug:
        def test_issue_1234(self, celery_setup: CeleryTestSetup):
            assert identity.s("test_issue_1234").apply_async(queue=celery_setup.worker.worker_queue).get() == "test_issue_1234"

.. warning::

    The smoke tests worker is **not** using the default ``celery`` queue and require using the ``queue`` argument to specify the worker queue
    when publishing tasks.

Signal Handlers
###############

Signals can be connected inline in the test case, or by injecting a module with the signal handlers into the worker.

Inline handlers can be used like this:

.. code-block:: python

    def test_issue_1234(self, celery_setup: CeleryTestSetup):
        @after_task_publish.connect
        def signal_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        signal_was_called = False
        noop.s().apply_async(queue=celery_setup.worker.worker_queue)
        assert signal_was_called is True

Injecting signal handlers is using a similar pattern to adding tasks and can be done according
to the :ref:`signal-handlers-modules-injection` section.

Tasks
~~~~~

The :ref:`default-tasks` can be used out-of-the-box, but you can also add new tasks to the worker by creating a new module
and injecting it into the environment. See :ref:`injecting-tasks` for more information.

Templates
=========

.. versionadded:: 1.0.0

Standalone Test Snippet
~~~~~~~~~~~~~~~~~~~~~~~

The following snippet can be used as a starting point for a bug report script. To use it, just copy and paste it into a
new file and run it with pytest.

The snippet is also part of the `CI system <https://github.com/celery/pytest-celery/actions/workflows/examples.yml>`_.

RabbitMQ Management Broker
--------------------------

We'll use the ``rabbitmq:management`` label to run the RabbitMQ broker with the management plugin for easy debugging.

Redis Backend
-------------

We'll use the Redis backend for simplicity.

Built-in Worker
---------------

We'll use the :ref:`built-in-worker` to use a specific Celery release.

.. literalinclude:: ../../examples/celery_bug_report.py
    :language: python
    :caption: examples.celery_bug_report.py

Execute with Pytest
###################

1. Create a new file, for example ``test_issue_1234.py``.
2. Copy and paste the snippet into the new file.
3. Install the plugin.
4. Run the test with pytest.

.. code-block:: console

    pip install -U "pytest-celery[all]"
    pytest -xsv test_issue_1234.py

You can run it from anywhere that has access to pull docker images, the plugin will take care of the rest.

Smoke Test Snippet
~~~~~~~~~~~~~~~~~~

The following snippet can be used as a starting point for a bug report script. To use it, just copy and paste it into a
new file in `t/smoke/tests <https://github.com/celery/celery/tree/main/t/smoke/tests>`_ and run it with tox or pytest.

RabbitMQ Management Broker
--------------------------

We'll use the ``rabbitmq:management`` label to run the RabbitMQ broker with the management plugin for easy debugging.

Redis Backend
-------------

We'll use the Redis backend for simplicity.

Smoke Tests Worker
------------------

We'll use the smoke tests worker to run the worker from the source code.

.. code-block:: python

    # flake8: noqa

    from __future__ import annotations

    import pytest
    from celery import Celery
    from celery.canvas import Signature
    from celery.result import AsyncResult
    from pytest_docker_tools import build
    from t.integration.tasks import identity
    from t.smoke.workers.dev import SmokeWorkerContainer

    from pytest_celery import RABBITMQ_PORTS
    from pytest_celery import CeleryBackendCluster
    from pytest_celery import CeleryBrokerCluster
    from pytest_celery import CeleryTestSetup
    from pytest_celery import RabbitMQContainer
    from pytest_celery import RabbitMQTestBroker
    from pytest_celery import RedisTestBackend

    ###############################################################################
    # RabbitMQ Management Broker
    ###############################################################################


    class RabbitMQManagementTestBroker(RabbitMQTestBroker):
        def get_management_url(self) -> str:
            """Opening this link during debugging allows you to see the
            RabbitMQ management UI in your browser.
            """
            ports = self.container.attrs["NetworkSettings"]["Ports"]
            ip = ports["15672/tcp"][0]["HostIp"]
            port = ports["15672/tcp"][0]["HostPort"]
            return f"http://{ip}:{port}"


    @pytest.fixture
    def default_rabbitmq_broker_image() -> str:
        return "rabbitmq:management"


    @pytest.fixture
    def default_rabbitmq_broker_ports() -> dict:
        # Expose the management UI port
        ports = RABBITMQ_PORTS.copy()
        ports.update({"15672/tcp": None})
        return ports


    @pytest.fixture
    def celery_rabbitmq_broker(default_rabbitmq_broker: RabbitMQContainer) -> RabbitMQTestBroker:
        broker = RabbitMQManagementTestBroker(default_rabbitmq_broker)
        yield broker
        broker.teardown()


    @pytest.fixture
    def celery_broker_cluster(celery_rabbitmq_broker: RabbitMQTestBroker) -> CeleryBrokerCluster:
        cluster = CeleryBrokerCluster(celery_rabbitmq_broker)
        yield cluster
        cluster.teardown()


    ###############################################################################
    # Redis Result Backend
    ###############################################################################


    @pytest.fixture
    def celery_backend_cluster(celery_redis_backend: RedisTestBackend) -> CeleryBackendCluster:
        cluster = CeleryBackendCluster(celery_redis_backend)
        yield cluster
        cluster.teardown()


    @pytest.fixture
    def default_redis_backend_image() -> str:
        return "redis:latest"


    ###############################################################################
    # Worker Configuration
    ###############################################################################


    class WorkerContainer(SmokeWorkerContainer):
        @classmethod
        def log_level(cls) -> str:
            return "INFO"

        @classmethod
        def worker_queue(cls) -> str:
            return "celery"

        @classmethod
        def command(cls, *args: str) -> list[str]:
            return super().command(
                "--without-gossip",
                "--without-mingle",
                "--without-heartbeat",
            )


    @pytest.fixture
    def default_worker_container_cls() -> type[SmokeWorkerContainer]:
        return WorkerContainer


    @pytest.fixture(scope="session")
    def default_worker_container_session_cls() -> type[SmokeWorkerContainer]:
        return WorkerContainer


    celery_dev_worker_image = build(
        path=".",
        dockerfile="t/smoke/workers/docker/dev",
        tag="t/smoke/worker:dev",
        buildargs=WorkerContainer.buildargs(),
    )


    @pytest.fixture
    def default_worker_app(default_worker_app: Celery) -> Celery:
        app = default_worker_app
        # app.conf...  # Add any additional configuration here
        return app


    ###############################################################################
    # Bug Reproduction
    ###############################################################################


    def test_issue_1234(celery_setup: CeleryTestSetup):
        sig: Signature = identity.s("test_issue_1234")
        res: AsyncResult = sig.delay()
        assert res.get() == "test_issue_1234"

Execute with Tox
################

1. Create a new file in `t/smoke/tests <https://github.com/celery/celery/tree/main/t/smoke/tests>`_, for example ``test_issue_1234.py``.
2. Copy and paste the snippet into the new file.
3. Run the test with tox.

.. code-block:: console

    tox -e 3.12-smoke -- -k test_issue_1234

Execute with Pytest
###################

1. Create a new file in `t/smoke/tests <https://github.com/celery/celery/tree/main/t/smoke/tests>`_, for example ``test_issue_1234.py``.
2. Copy and paste the snippet into the new file.
3. Install the required dependencies.
4. Run the test with pytest.

.. code-block:: console

    pip install -e .
    pip install -r requirements/test.txt
    pytest -xsv t/smoke -k test_issue_1234

Make sure to run it from the root of the Celery repository.
