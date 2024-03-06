.. _vendors:

=========
 Vendors
=========

:Release: |version|
:Date: |today|

.. contents::
    :local:
    :depth: 2

Built-in Brokers and Backends
=============================

The plugin comes with support for several brokers and backends out of
the box.  This page lists the supported vendors and their status.

Brokers
~~~~~~~

+---------------+--------------+--------------+
| **Name**      | **Status**   | **Enabled**  |
+---------------+--------------+--------------+
| *RabbitMQ*    | Stable       | Yes          |
+---------------+--------------+--------------+
| *Redis*       | Stable       | Yes          |
+---------------+--------------+--------------+

Backends
~~~~~~~~

+---------------+--------------+--------------+
| **Name**      | **Status**   | **Enabled**  |
+---------------+--------------+--------------+
| *Redis*       | Stable       | Yes          |
+---------------+--------------+--------------+
| *Memcache*    | Experimental | No           |
+---------------+--------------+--------------+

Experimental brokers may be functional but are not confirmed to be
production ready.

Enabled means that it is automatically added to the test :ref:`setup-matrix`
when running the test suite :ref:`if the vendor dependencies are installed <installation>`.

.. warning::

    Enabling a new vendor will automatically add it globally to every test suite that relies
    on the default vendors detection. Be careful when enabling new vendors and make sure they are
    stable and production ready.

.. _built-in-worker:

Built-in Celery Worker
======================

The plugin provides a built-in Celery worker that can be used to run
tests against. It uses the latest stable version of Celery and can be used, replaced or extended
by the user.

The Dockerfile is published with the source code and can be found using
:const:`WORKER_DOCKERFILE_ROOTDIR <pytest_celery.vendors.worker.defaults.WORKER_DOCKERFILE_ROOTDIR>`.

.. literalinclude:: ../../src/pytest_celery/vendors/worker/Dockerfile
   :language: docker
   :caption: pytest_celery.vendors.worker.Dockerfile

.. _custom-vendors:

Custom Vendors
==============

Injected brokers, backends and workers can extend the built-in ones or
provide completely new ones. The plugin provides a set of base classes
that can be used to implement custom vendors.

Custom Broker
~~~~~~~~~~~~~

.. autoclass:: pytest_celery.api.broker.CeleryTestBroker
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :no-index:

Custom Backend
~~~~~~~~~~~~~~

.. autoclass:: pytest_celery.api.backend.CeleryTestBackend
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :no-index:

Custom Worker
~~~~~~~~~~~~~

.. autoclass:: pytest_celery.api.worker.CeleryTestWorker
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :no-index:

.. _vendor-class:

Vendor Class
============

The **Vendor Class** is an optional mechanism for OOP style configuration of the plugin's vendors.
It allows registering a class that defines how does the vendor behave and configured.

The vendor class represents the vendor's container class that is used automatically by the plugin.

The following diagram shows the relationship between the vendor class and the vendor's infrastructure.

.. mermaid::

    graph TD;
        Vendor[Vendor] --> BrokerComponent[Broker Component]
        Vendor --> BackendComponent[Backend Component]
        Vendor --> WorkerComponent[Worker Component]

        BrokerComponent --> Comp
        BackendComponent --> Comp
        WorkerComponent --> Comp

        subgraph Comp["Component"]
            Node[Node] --> Container[Container]
        end

        Comp --> DefaultFixtures[Default Fixtures]
        Comp --> VendorClass[Vendor Class]
        VendorClass -. "You are here" .-> VendorClass
        DefaultFixtures <.-> VendorClass

        style Vendor fill:#f9f,stroke:#333,stroke-width:4px
        style Comp fill:#ddf,stroke:#333,stroke-width:2px
        style Node fill:#eeffdd,stroke:#333
        style Container fill:#ffffee,stroke:#333
        style VendorClass fill:#ffeedd,stroke:#333

Use Cases
~~~~~~~~~

.. warning::

    It is used only to override the built-in vendors **containers**.

Registering a Vendor Class
--------------------------

The plugin uses the vendor class to implement the default fixtures of the vendor.
To override it, create your own vendor class and subclass the matching built-in vendor class
to include the built-in fixtures implementation.

Worker Example
##############

.. code-block:: python

    class MyWorkerContainer(CeleryWorkerContainer):
        @property
        def client(self) -> Any:
            return self

        @classmethod
        def version(cls) -> str:
            return celery.__version__

        @classmethod
        def log_level(cls) -> str:
            return "INFO"

        @classmethod
        def worker_name(cls) -> str:
            return "my_tests_worker"

        @classmethod
        def worker_queue(cls) -> str:
            return "my_tests_queue"

        def post_initialization_logic(self) -> None:
            pass

And then, register it using the matching default fixture.

.. code-block:: python

    @pytest.fixture
    def default_worker_container_cls() -> Type[CeleryWorkerContainer]:
        return MyWorkerContainer

.. warning::

    The worker vendor requires another fixture to be registered to allow configuring the worker
    before it gets built.

.. code-block:: python

    @pytest.fixture(scope="session")
    def default_worker_container_session_cls() -> Type[CeleryWorkerContainer]:
        return MyWorkerContainer

There's no ``session`` vendor class for other vendors.

- For RabbitMQ Broker use :func:`default_rabbitmq_broker_cls <pytest_celery.vendors.rabbitmq.fixtures.default_rabbitmq_broker_cls>`.
- For Redis Broker use :func:`default_redis_broker_cls <pytest_celery.vendors.redis.broker.fixtures.default_redis_broker_cls>`.
- For Redis Backend use :func:`default_redis_backend_cls <pytest_celery.vendors.redis.backend.fixtures.default_redis_backend_cls>`.
- For Memcache Backend use :func:`default_memcached_backend_cls <pytest_celery.vendors.memcached.fixtures.default_memcached_backend_cls>`.

Accessing the Vendor Class
--------------------------

Once a vendor class has been registered, it can be accessed using the :ref:`test-setup`.
Any additional API added to the class can be accessed as well.

For example,

.. code-block:: python

    def test_accessing_post_initialization_logic(celery_setup: CeleryTestSetup):
        worker: MyWorkerContainer = celery_setup.worker
        worker.post_initialization_logic()
