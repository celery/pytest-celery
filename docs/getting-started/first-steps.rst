.. _first-steps:

================================
 First Steps with pytest-celery
================================

:Release: |version|
:Date: |today|

The pytest-celery plugin is a test framework for Celery applications.
It encapsulates the complexity of setting up a test environment, and provides a simple way to write tests for your Celery applications.

This tutorial will guide you through the first steps of using pytest-celery.
It will explain the basic concepts and show you how to write your first test.

.. note::

    This tutorial assumes that you have a basic understanding of Celery and pytest.
    If you are new to Celery, you should read the `Celery documentation <http://docs.celeryproject.org/en/latest/>`_ first.
    If you are new to pytest, you should read the `pytest documentation <https://docs.pytest.org/en/latest/>`_ first.

.. contents::
    :local:
    :depth: 2

Understanding the Environment
=============================

When testing a Celery application, we want to ensure we prepare the right environment for each test to
allow focusing on the test case itself and extract the logic behind the setting up of the environment.
The plugin uses the pytest fixtures mechanism to provide a way to control the environment and the test
matrix for each test case.

Components
~~~~~~~~~~

The environment has the following main components.

- **Celery Worker**: The worker is the main component of the Celery application. It is responsible for executing the tasks.
- **Broker**: The broker is the message queue that the worker uses to receive tasks.
- **Result Backend**: The result backend is the storage where the worker stores the results of the tasks.

By default, every test case is executed against all of the (enabled) :ref:`built-in vendors <vendors>`,
using the latest Celery version.

Environment Layers
~~~~~~~~~~~~~~~~~~

The test environment is composed of several layers, each of which can be controlled by the user.

.. _test-containers:

Test Containers
---------------

This is considered the lowest layer, and is responsible for managing docker container instances.
It is used to describe a docker container and manage its lifecycle.

To represent a ``Dockerfile`` within the environment, implement a class that inherits from
:class:`CeleryTestContainer <pytest_celery.api.container.CeleryTestContainer>`.

The class is Celery-agnostic, and can be used to represent any container that is required for the test environment.

There are three main types of containers.

- :class:`Worker Container <pytest_celery.vendors.worker.container.CeleryWorkerContainer>`: Base class for Celery worker containers.
- :class:`RabbitMQ Container <pytest_celery.vendors.rabbitmq.container.RabbitMQContainer>`: Base class for RabbitMQ containers.
- :class:`Redis Container <pytest_celery.vendors.redis.container.RedisContainer>`: Base class for Redis containers.

These classes are Context-aware, and can be used to represent a container for their domain in the environment.

.. _test-nodes:

Test Nodes
----------

A test node is the logical representation of a :ref:`test container <test-containers>`.
It encapsulates the logic of a specific context and provides useful APIs to interact with the container.

To represent a node within the environment, implement a class that inherits from
:class:`CeleryTestNode <pytest_celery.api.base.CeleryTestNode>`.

There are three main types of nodes.

- :class:`Test Worker <pytest_celery.api.worker.CeleryTestWorker>`: Represents a Celery worker instance.
- :class:`Test Broker <pytest_celery.api.broker.CeleryTestBroker>`: Represents a broker instance.
- :class:`Test Backend <pytest_celery.api.backend.CeleryTestBackend>`: Represents a result backend instance.

All nodes are interchangeable within their domain, allowing plug-and-play style configuration when setting up
the test environment. A node responsible for a specific component can be replaced with another node responsible
for the same component, and the test environment will continue to function as expected, following the
`Liskov Substitution Principle <https://en.wikipedia.org/wiki/Liskov_substitution_principle>`_.

Under this principle, the test environment is designed to be flexible and extensible, allowing the user to
easily replace any component with a custom implementation.

.. _test-clusters:

Test Clusters
-------------

A test cluster is a collection of test nodes for a certain domain.
**It is used as the entry point for the nodes into the test environment.**

To represent a cluster within the environment, implement a class that inherits from
:class:`CeleryTestCluster <pytest_celery.api.base.CeleryTestCluster>`.

A test case does not load nodes directly, but rather loads a cluster, which in turn loads the nodes.
By default, single-node clusters are used, but the user can define custom clusters to load multiple nodes.

There are three main types of clusters.

- :class:`Worker Cluster <pytest_celery.api.worker.CeleryWorkerCluster>`: Represents a cluster of Celery workers.
- :class:`Broker Cluster <pytest_celery.api.broker.CeleryBrokerCluster>`: Represents a cluster of brokers.
- :class:`Backend Cluster <pytest_celery.api.backend.CeleryBackendCluster>`: Represents a cluster of result backends.

.. _test-setup:

Test Setup
----------

A test setup is the highest layer of the environment.
**It is the main entry point for the test environment and is responsible for loading
the clusters and preparing the environment for the test case.**

To represent a setup within the environment, implement a class that inherits from
:class:`CeleryTestSetup <pytest_celery.api.setup.CeleryTestSetup>`.

.. note::
    By default, the default setup is configured by individually configuring each component in the environment
    and overriding it is not required in most cases.
    Creating your own class allows global overrides in a centralized place and is recommended
    only for advanced use cases. For most cases, configuring each component individually is sufficient.

The test setup will be the specific permutation of the environment matrix used for a
specific test run. Every test case running on a matrix of possible architectures
will access its components via the test setup instance for its test session.

Every test case that uses a test setup will automatically inherit the matrix of architectures
for that setup and will access each combination in isolation per test run.

This simple test then,

.. code-block:: python

    def test_hello_world(celery_setup: CeleryTestSetup):
        assert celery_setup.ready()

Will run against all of the (enabled) possible combinations of the environment matrix.

.. code-block:: console

    pytest tests/test_example.py
    ======================================================================= test session starts ===================================
    ...

    tests/test_example.py::test_hello_world[celery_setup_worker-celery_rabbitmq_broker-celery_redis_backend] PASSED         [ 50%]
    tests/test_example.py::test_hello_world[celery_setup_worker-celery_redis_broker-celery_redis_backend] PASSED            [100%]

    ...
    ======================================================================= 2 passed in 22.78s ====================================

With each iteration having its own isolated environment.

RabbitMQ Broker Iteration Breakdown
###################################

.. code-block:: console

    docker ps
    CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS          PORTS                                                                     NAMES
    0ffb4e75b5e4   c9ef6c81f5dc      "/bin/sh -c 'celery …"   30 seconds ago   Up 29 seconds                                                                             upbeat_feistel
    ac085d253cda   redis:latest      "docker-entrypoint.s…"   31 seconds ago   Up 30 seconds   0.0.0.0:64057->6379/tcp                                                   gallant_carson
    deeb60b73af5   rabbitmq:latest   "docker-entrypoint.s…"   36 seconds ago   Up 35 seconds   4369/tcp, 5671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:64056->5672/tcp   romantic_cannon

With the worker configured correctly for its broker and backend.

.. code-block:: console

     -------------- celery_test_worker@0ffb4e75b5e4 v5.3.6 (emerald-rush)
    --- ***** -----
    -- ******* ---- Linux-6.6.12-linuxkit-aarch64-with-glibc2.28 2024-02-04 12:05:15
    - *** --- * ---
    - ** ---------- [config]
    - ** ---------- .> app:         celery_test_app:0xffffba454d90
    - ** ---------- .> transport:   amqp://guest:**@deeb60b73af5:5672//
    - ** ---------- .> results:     redis://ac085d253cda/0
    - *** --- * --- .> concurrency: 10 (prefork)
    -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
    --- ***** -----
     -------------- [queues]
                    .> celery           exchange=celery(direct) key=celery

With more verbose test logs.

.. code-block:: console

    ============================= test session starts ==============================
    ...

    tests/test_example.py::test_hello_world[celery_setup_worker-celery_rabbitmq_broker-celery_redis_backend] Creating network pytest-73fadda9-8fed-401c-a0f9-78e9108818a4
    Waiting for container to be ready......RabbitMQContainer::romantic_cannon is ready.
    Waiting for container to be ready.RedisContainer::gallant_carson is ready.
    Creating volume pytest-0d0ed18e-ae68-4d10-80d4-2d46ccd6d9a7
    Building [REDUCTED]/site-packages/pytest_celery/vendors/worker......................................................................
    Waiting for container to be ready.Waiting for CeleryWorkerContainer::upbeat_feistel to get ready...
    CeleryWorkerContainer::upbeat_feistel is ready.
    RabbitMQContainer::romantic_cannon is ready.
    RedisContainer::gallant_carson is ready.
    CeleryWorkerContainer::upbeat_feistel is ready.
    PASSED

    ======================== 1 passed in 282.12s (0:04:42) =========================

Redis Broker Iteration Breakdown
################################

.. code-block:: console

    docker ps
    CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                     NAMES
    37e8ea35206f   c9ef6c81f5dc   "/bin/sh -c 'celery …"   28 seconds ago   Up 27 seconds                             adoring_diffie
    5364f8bc75f1   redis:latest   "docker-entrypoint.s…"   28 seconds ago   Up 27 seconds   0.0.0.0:64235->6379/tcp   beautiful_bouman
    65fe26ddcd10   redis:latest   "docker-entrypoint.s…"   29 seconds ago   Up 28 seconds   0.0.0.0:64234->6379/tcp   reverent_mendeleev

With the worker configured correctly for its broker and backend.

.. code-block:: console

     -------------- celery_test_worker@37e8ea35206f v5.3.6 (emerald-rush)
    --- ***** -----
    -- ******* ---- Linux-6.6.12-linuxkit-aarch64-with-glibc2.28 2024-02-04 12:15:01
    - *** --- * ---
    - ** ---------- [config]
    - ** ---------- .> app:         celery_test_app:0xffffa4f18d90
    - ** ---------- .> transport:   redis://65fe26ddcd10:6379/0
    - ** ---------- .> results:     redis://5364f8bc75f1/0
    - *** --- * --- .> concurrency: 10 (prefork)
    -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
    --- ***** -----
     -------------- [queues]
                    .> celery           exchange=celery(direct) key=celery

With more verbose test logs.

.. code-block:: console

    ============================= test session starts ==============================
    ...

    tests/test_example.py::test_hello_world[celery_setup_worker-celery_redis_broker-celery_redis_backend] Building [REDUCTED]/site-packages/pytest_celery/vendors/worker......................................................................
    Creating network pytest-134ab26c-2fa0-457b-b451-7c9f282760dd
    Waiting for container to be ready.RedisContainer::reverent_mendeleev is ready.
    Waiting for container to be ready.RedisContainer::beautiful_bouman is ready.
    Creating volume pytest-bfff6a4a-31c7-4729-8001-0d6197095460
    Waiting for container to be ready.Waiting for CeleryWorkerContainer::adoring_diffie to get ready........
    CeleryWorkerContainer::adoring_diffie is ready.
    RedisContainer::reverent_mendeleev is ready.
    RedisContainer::beautiful_bouman is ready.
    CeleryWorkerContainer::adoring_diffie is ready.
    PASSED

    ======================== 1 passed in 105.89s (0:01:45) =========================

Vendors
~~~~~~~

The term "vendors" is used to describe the built-in components that are provided by the plugin.
The currently available vendors and their status are described in the :ref:`vendors <vendors>` section.

Each vendor can be tested separately, for independent testing of each component.

For example, testing the :ref:`default redis broker <redis-broker>` container by itself.

.. code-block:: python

    class test_redis_container:
        def test_the_underlying_container(self, default_redis_broker: RedisContainer):
            container = default_redis_broker
            assert container.client
            assert container.client.ping()
            assert container.client.set("ready", "1")
            assert container.client.get("ready") == "1"
            assert container.client.delete("ready")

Or, testing the :ref:`default redis broker <redis-broker>` at the node level.

.. code-block:: python

    class test_redis_test_broker:
        def test_the_redis_broke_node(self, celery_redis_broker: RedisTestBroker):
            container: RedisContainer = celery_redis_broker.container
            assert container.client
            assert container.client.ping()
            assert container.client.set("ready", "1")
            assert container.client.get("ready") == "1"
            assert container.client.delete("ready")

Remember, each test case is isolated. This means that both of these tests
can run in parallel, and **each will be assigned its own container instance.**

.. code-block:: console

    pytest tests/test_example.py -n auto
    ======================================================================= test session starts ===================================
    ...

    tests/test_example.py::Test_redis_test_broker::test_the_redis_broke_node
    tests/test_example.py::Test_redis_container::test_the_underlying_container
    [gw1] [ 50%] PASSED tests/test_example.py::Test_redis_test_broker::test_the_redis_broke_node
    [gw0] [100%] PASSED tests/test_example.py::Test_redis_container::test_the_underlying_container

    ======================================================================== 2 passed in 1.72s ====================================

.. code-block:: console

    docker ps
    CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                     NAMES
    b1c1f793484d   redis:latest   "docker-entrypoint.s…"   4 seconds ago   Up 3 seconds   0.0.0.0:65110->6379/tcp   frosty_tu
    29f69833fe49   redis:latest   "docker-entrypoint.s…"   4 seconds ago   Up 3 seconds   0.0.0.0:65109->6379/tcp   eager_agnesi

Summary
~~~~~~~

Before we can learn how to fit the environment to our needs, let's have a quick recap over what we just learned in this section.

.. list-table::
   :widths: 30 70

   * - **Core Components**
     - The environment is built around three key components: the Celery worker, a broker, and a backend, each within their respective containers, nodes, and clusters.
   * - **Lifecycle Management**
     - Containers and nodes manage the lifecycle of components, assembling them into clusters for the test setup.
   * - **Independent Nodes**
     - Nodes function independently, enhancing flexibility in testing, configuration, and customization for specific project requirements.
   * - **Main Entry Point**
     - All of the given components integrate into the test setup, which is the main entry point for the test environment.
   * - **Modular Approach**
     - All nodes are interchangeable within their domain, allowing plug-and-play style configuration when setting up the test environment.
   * - **Isoalted Environments**
     - Each test case has its own instances of the environment, allowing for parallelism and isolation of test cases.

.. _manipulating-the-environment:

Manipulating the Environment
============================

The plugin provides a set of fixtures that can be used to control the environment.
These fixtures are responsible for initializing the test nodes and creating the test setup which in turn
generates a matrix of environments for each test case.

.. _default-fixtures:

Default Fixtures
~~~~~~~~~~~~~~~~

Each component of the setup has its own `parameterized fixtures set <https://docs.pytest.org/en/latest/how-to/parametrize.html>`_.
These fixtures are responsible for generating the environment matrix and providing the test nodes for each test case.

Each of these components can be independently manipulated by hooking into the matching ``default_`` fixtures of the component,
as some of the following examples will show.

Test Worker
~~~~~~~~~~~

These fixtures will generate a cluster with a single Celery worker node, based on the :ref:`built-in Dockerfile <built-in-worker>`.

1. :func:`celery_worker <pytest_celery.fixtures.worker.celery_worker>`: Latest Celery worker node.
2. :func:`celery_worker_cluster <pytest_celery.fixtures.worker.celery_worker_cluster>`: Single worker cluster for ``celery_worker``.

.. _celery-application:

Celery Application
-------------------

The Celery app can be controlled by hooking into the :func:`default_worker_app <pytest_celery.vendors.worker.fixtures.default_worker_app>` fixture.
For example, we can control worker configuration like this:

.. code-block:: python

    @pytest.fixture
    def default_worker_app(default_worker_app: Celery) -> Celery:
        app = default_worker_app
        app.conf.worker_prefetch_multiplier = 1
        app.conf.worker_concurrency = 1
        return app

And every test in the `scope of this fixture <https://docs.pytest.org/en/latest/reference/fixtures.html#fixture-availability>`_ will use the modified app.

In addition, the changed configuration will be printed for debug purposes before the Celery banner.
Only changed fields will be shown.

.. code-block:: text

    Changed worker configuration: {
        "worker_prefetch_multiplier": 1,
        "worker_concurrency": 1
    }

     -------------- celery_test_worker@c5a0c3dbf9c2 v5.3.6 (emerald-rush)
    --- ***** -----
    -- ******* ---- Linux-6.6.12-linuxkit-aarch64-with-glibc2.36 2024-02-04 17:36:52
    - *** --- * ---
    - ** ---------- [config]
    - ** ---------- .> app:         celery_test_app:0xffffb82dc990
    - ** ---------- .> transport:   amqp://guest:**@825303d1a340:5672//
    - ** ---------- .> results:     redis://5849b4a867b1/0
    - *** --- * --- .> concurrency: 1 (prefork)
    -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
    --- ***** -----
     -------------- [queues]
                    .> celery           exchange=celery(direct) key=celery

.. note::

    By default, the same Celery app instance is shared across all the setup nodes
    per isolated environment.

Tasks
-----

The available tasks can be controlled by hooking into the :func:`default_worker_tasks <pytest_celery.vendors.worker.fixtures.default_worker_tasks>` fixture.
The plugin adds a :func:`ping task <pytest_celery.vendors.worker.tasks.ping>` by default, but you can add your own tasks like this:

.. code-block:: python

    @pytest.fixture
    def default_worker_tasks(default_worker_tasks: set) -> set:
        from tests import tasks

        default_worker_tasks.add(tasks)
        return default_worker_tasks

Signals
-------

Signals handlers that needs to be injected into the worker, can be added by hooking into
the :func:`default_worker_signals <pytest_celery.vendors.worker.fixtures.default_worker_signals>` fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_signals(default_worker_signals: set) -> set:
        from tests import signals

        default_worker_signals.add(signals)
        return default_worker_signals

For handlers inside the test, you can use the standard API, for example.

.. code-block:: python

    from celery.signals import before_task_publish

    def test_before_task_publish(celery_setup: CeleryTestSetup):
        @before_task_publish.connect
        def before_task_publish_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        signal_was_called = False
        mytask.s().apply_async()
        assert signal_was_called is True

Test Broker
~~~~~~~~~~~

These fixtures will generate a cluster with a single broker node, for each enabled broker :ref:`vendor <vendors>`.
The test case will be parameterized for each available broker.

1. :func:`celery_broker <pytest_celery.fixtures.broker.celery_broker>`: Parameterized fixture for all of the available brokers nodes.
2. :func:`celery_broker_cluster <pytest_celery.fixtures.broker.celery_broker_cluster>`: Single broker cluster for ``celery_broker``.

The :ref:`RabbitMQ Management Example <examples_rabbitmq-management>` provides a good demonstration of how to override the default broker configuration,
with a single ``rabbitmq:management`` broker instead of the broker matrix.

Test Backend
~~~~~~~~~~~~

These fixtures will generate a cluster with a single backend node, for each enabled backend :ref:`vendor <vendors>`.
The test case will be parameterized for each available backend.

1. :func:`celery_backend <pytest_celery.fixtures.backend.celery_backend>`: Parameterized fixture for all of the available backends nodes.
2. :func:`celery_backend_cluster <pytest_celery.fixtures.backend.celery_backend_cluster>`: Single backend cluster for ``celery_backend``.

.. _disable_backend:

Disabling the Backend
---------------------

The design principle is simple - if there's no backend instance available, then there's nothing to plug into the setup.

.. code-block:: python

    @pytest.fixture
    def celery_backend_cluster():
        return None

This snippet will tell pytest-celery to skip the backend setup for the matching tests.

.. warning::

    Disabling the backend will disable the result backend for the worker, and the worker will not be able to store the results of the tasks.

    **This may cause hangs when calling get() on the results!**

.. note::

    Yes, you can also do it with the broker and worker clusters, but it doesn't make sense in general.
    That being said, the plugin will not prevent you from doing so.

Test Setup
~~~~~~~~~~

Each component of the setup can be configured independently to allow modular control of the setup.
Eventually, all of the components will be combined into the :func:`celery_setup <pytest_celery.fixtures.setup.celery_setup>` fixture, as
discussed :ref:`before <test-setup>`.

Generally, the user should not hook into the ``celery_setup`` fixture directly.
Hooking into the individual components is the recommended way to control the environment.

Hooking into the ``celery_setup`` fixture is only recommended for advanced use cases, and is not required in most cases.

Summary
~~~~~~~

In the previous section, we learned which components compose the test setup environment.
This section, introduced us to the plugin's mechanism to manipulate and configure those components using their :ref:`default fixtures <default-fixtures>`.

Let's have a quick recap over what we just learned in this section then.

.. list-table::
   :widths: 30 70

   * - **Parameterized Fixtures**
     - Each component of the setup has its own parameterized fixtures set, one for the node and one for the cluster.
   * - **Configurable Components**
     - Each default component has its ``default_`` fixtures list, which can be used to control or extend the component's functionality.
   * - **Setup Matrix**
     - The :func:`celery_setup <pytest_celery.fixtures.setup.celery_setup>` will generate a :ref:`setup-matrix` of isolated environments for each test case, based on the enabled components and their configurations.

.. _built-in-components:

Using the built-in components
=============================

The built-in components are designed under their own layers and follow a similar pattern.
Each built-in component provides a complete package, encapsulating all of the elements of the component.

These components can be used for standard use cases, reconfigured for more complex cases,
or entirely replaced by a set of components specific to the target project.

.. tip::

    The built-in components are designed to be flexible and extensible and can be used as a starting point for custom setups.
    Make the most straightforward setup for a test case to avoid over-engineering the test environment.
    Reconfiguring the existing components is very powerful and should be the first step in most cases.

.. _components-layers:

Components Layers
~~~~~~~~~~~~~~~~~

Each components is defined by several layers.
Each of these layers can be replaced or reconfigured to fit the needs of the target project.

.. tip::

    Feel free to experiment with the built-in components to understand how they work and adjust them to your needs.
    Use the :ref:`examples` as a starting point for your POCs; it can be very useful for practicing the concepts of this guide.

Container
---------

The container class is responsible for managing the lifecycle of the container instance.
It is used to control the container instance and encapsulate the container-specific implementation.
Each docker image should have a corresponding container class, regardless of the runtime configuration for the container
(e.g., the same docker image may have more than one container class for scoping it into different domains).

For additional documentation, see `pytest-docker-tools documentation <https://github.com/Jc2k/pytest-docker-tools?tab=readme-ov-file#containers>`_.

.. warning::

    The test tears down the docker containers after the test case is finished, regardless of the test result.
    Stopping a test during execution though may leak test resources into the host machine and require manual cleanup afterward.

    Avoiding cleanup may cause random test failures due to lack of docker resources on the host machine. The plugin
    will gracefully wait for resources for a limited time before failing in such case.

Node
----

A node instance contains a container instance and provides a set of APIs to interact with the container.
A node can be loaded into the test environment via a cluster in the setup, or directly by itself.

Every component needs a node representation to be part of a setup.

All of the built-in nodes are based on the :ref:`test-nodes` classes.

Defaults
--------

Each component has a ``defaults.py`` module that contains the default configuration for the component.
The module is a list of settings that are used to initialize the component.

Fixtures
--------

All of the built-in fixtures are using the ``default_`` prefix.
Each component has **at least** two fixtures, one for the container and one for the node.
These fixtures are responsible for the setup/teardown of each node.

Built-in Components
~~~~~~~~~~~~~~~~~~~

.. _celery-worker:

Celery Worker
-------------

The built-in worker is a special worker, designed for bootstrapping the test environment.
It uses the latest Celery release and its own :ref:`Dockerfile <built-in-worker>`.

Container
#########

The :class:`CeleryWorkerContainer <pytest_celery.vendors.worker.container.CeleryWorkerContainer>` is used
to describe the :ref:`built-in-worker`.

Node
####

The :class:`CeleryTestWorker <pytest_celery.api.worker.CeleryTestWorker>` is used to represent the worker node.

Fixtures
########

A list of available fixtures for the worker can be found in the :mod:`pytest_celery.vendors.worker.fixtures` module.

.. _rabbitmq-broker:

RabbitMQ Broker
---------------

The RabbitMQ broker uses the ``rabbitmq:latest`` version for the underlying container.

Container
#########

The :class:`RabbitMQContainer <pytest_celery.vendors.rabbitmq.container.RabbitMQContainer>` is used
to describe the ``rabbitmq:latest`` docker image.

Node
####

The :class:`RabbitMQTestBroker <pytest_celery.vendors.rabbitmq.api.RabbitMQTestBroker>` is used to represent the broker node.

Fixtures
########

A list of available fixtures for the broker can be found in the :mod:`pytest_celery.vendors.rabbitmq.fixtures` module.

.. _redis-broker:

Redis Broker
------------

The Redis broker uses the ``redis:latest`` version for the underlying container.

Container
#########

The :class:`RedisContainer <pytest_celery.vendors.redis.container.RedisContainer>` is used
to describe the ``redis:latest`` docker image.

Node
####

The :class:`RedisTestBroker <pytest_celery.vendors.redis.broker.api.RedisTestBroker>` is used to represent the broker node.

Fixtures
########

A list of available fixtures for the broker can be found in the :mod:`pytest_celery.vendors.redis.broker.fixtures` module.

.. _localstack-broker:

Localstack (SQS) Broker
-----------------------

The Localstack broker uses the ``localstack/localstack`` version for the underlying container.

Container
#########

The :class:`LocalstackContainer <pytest_celery.vendors.localstack.container.LocalstackContainer>` is used
to describe the ``localstack/localstack`` docker image.

Node
####

The :class:`LocalstackTestBroker <pytest_celery.vendors.localstack.api.LocalstackTestBroker>` is used to represent the broker node.

Fixtures
########

A list of available fixtures for the broker can be found in the :mod:`pytest_celery.vendors.localstack.fixtures` module.

.. _redis-backend:

Redis Backend
-------------

The Redis backend uses the ``redis:latest`` version for the underlying container.

Container
#########

The :class:`RedisContainer <pytest_celery.vendors.redis.container.RedisContainer>` is used
to describe the ``redis:latest`` docker image.

Node
####

The :class:`RedisTestBackend <pytest_celery.vendors.redis.backend.api.RedisTestBackend>` is used to represent the backend node.

Fixtures
########

A list of available fixtures for the backend can be found in the :mod:`pytest_celery.vendors.redis.backend.fixtures` module.

.. _memcached-backend:

Memcached Backend
-----------------

The Memcached backend uses the ``memcached:latest`` version for the underlying container.

Container
#########

The :class:`MemcachedContainer <pytest_celery.vendors.memcached.container.MemcachedContainer>` is used
to describe the ``memcached:latest`` docker image.

Node
####

The :class:`MemcachedTestBackend <pytest_celery.vendors.memcached.api.MemcachedTestBackend>` is used to represent the backend node.

Fixtures
########

A list of available fixtures for the backend can be found in the :mod:`pytest_celery.vendors.memcached.fixtures` module.

.. warning::

    The Memcached backend component is current experimental.

    Please :ref:`report <help>` any issues you encounter!

Summary
~~~~~~~

In the previous sections, we've covered which components compose the Celery test environment and how to construct
your own setup and configurations. We've seen :ref:`examples` that are using the built-in components and in this section,
we've discussed the general design of each component by itself.

Key takeaways from this section.

.. list-table::
   :widths: 30 70

   * - **Built-in Vendors**
     - The plugin provides a worker, borker and backend components out-of-the-box and generates a matrix of all possible combinations for each test case by default.
   * - **Component APIs**
     - Each component has container and node classes that provides an API for interacting with the component in the test case.
   * - **Component Fixtures**
     - Each component has a ``default_`` fixtures list that can be used to control or extend the component's functionality.
   * - **Extensible Design**
     - Most of the configurations can be overridden or extended to bootstrap the environment for the target project.

.. _hello-world:

Hello, World!
=============

If you followed this guide so far, you should be ready to write your first test case using the plugin!
Let's create a new, simple, non-parameterized setup using the built-in components and then write a simple test case for it.

Setting up the environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

First, we'll create a new ``tasks.py`` module and a new ``test_helloworld.py`` file.

Tasks
-----

This will be our ``tasks.py`` file. It adds a simple ``noop`` task
`Using the @shared_task decorator <https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-the-shared-task-decorator>`_.

.. code-block:: python

    import celery.utils
    from celery import shared_task


    @shared_task
    def noop(*args, **kwargs) -> None:
        return celery.utils.noop(*args, **kwargs)

Broker
------

Next, we'll configure a single broker setup using the built-in RabbitMQ broker, instead of using the default broker matrix.

.. tip::

    Try debugging this fixture and observe the ``celery_rabbitmq_broker`` and ``cluster`` objects.

.. code-block:: python

    @pytest.fixture
    def celery_broker_cluster(celery_rabbitmq_broker: RabbitMQTestBroker) -> CeleryBrokerCluster:
        cluster = CeleryBrokerCluster(celery_rabbitmq_broker)
        yield cluster
        cluster.teardown()

Backend
-------

Next, we'll configure a single backend setup using the built-in Redis backend, instead of using the default backend matrix.

.. code-block:: python

    @pytest.fixture
    def celery_backend_cluster(celery_redis_backend: RedisTestBackend) -> CeleryBackendCluster:
        cluster = CeleryBackendCluster(celery_redis_backend)
        yield cluster
        cluster.teardown()

.. tip::

    Try :ref:`disable_backend` to see how it affects the test case. Don't forget to remove the ``get()`` call.

Worker
------

We'll use the built-in worker, and we'll inject our ``tasks.py`` module from before so we can use it in our test case.

.. code-block:: python

    @pytest.fixture
    def default_worker_tasks(default_worker_tasks: set) -> set:
        from tests import tasks

        default_worker_tasks.add(tasks)
        return default_worker_tasks

.. note::

    We assume all files are under ``tests`` and all of the configurations are in the tests directory.
    They may live in other locations and the fixtures may move to ``conftest.py``.

Example Test Case
~~~~~~~~~~~~~~~~~

In our test case, we'll assert our setup is configured as expected, and publish our ``noop`` task to the setup test worker.

.. code-block:: python

    def test_hello_world(celery_setup: CeleryTestSetup):
        assert isinstance(celery_setup.broker, RabbitMQTestBroker)
        assert isinstance(celery_setup.backend, RedisTestBackend)
        assert noop.s().apply_async().get() is None

test_helloworld.py
~~~~~~~~~~~~~~~~~~

Sometimes the best way to learn is to get your hands dirty. This is why the hello world example was not included
in the :ref:`standard examples <examples>` section. Try to get it running on your own and experiment with it.
Create a simple new project and try debugging the test case to understand how the environment is set up.

.. tip::

    The pytest-celery API is fully annotated.
    Use your IDE's autocomplete feature to explore the available methods and classes.

.. code-block:: python

    import pytest

    from pytest_celery import CeleryBrokerCluster
    from pytest_celery import CeleryTestSetup
    from pytest_celery import RabbitMQTestBroker
    from pytest_celery import RedisTestBroker
    from tests.tasks import noop


    @pytest.fixture
    def celery_broker_cluster(celery_rabbitmq_broker: RabbitMQTestBroker) -> CeleryBrokerCluster:
        cluster = CeleryBrokerCluster(celery_rabbitmq_broker)
        yield cluster
        cluster.teardown()


    @pytest.fixture
    def celery_backend_cluster(celery_redis_broker: RedisTestBroker) -> CeleryBrokerCluster:
        cluster = CeleryBrokerCluster(celery_redis_broker)
        yield cluster
        cluster.teardown()


    @pytest.fixture
    def default_worker_tasks(default_worker_tasks: set) -> set:
        from tests import tasks

        default_worker_tasks.add(tasks)
        return default_worker_tasks


    def test_hello_world(celery_setup: CeleryTestSetup):
        assert isinstance(celery_setup.broker, RabbitMQTestBroker)
        assert isinstance(celery_setup.backend, RedisTestBroker)
        assert noop.s().apply_async().get() is None

Where to go from here
=====================

If you want to learn more you should continue to the :ref:`Next Steps <next-steps>` tutorial, and after that you
can read the :ref:`User Guide <userguide>`.
