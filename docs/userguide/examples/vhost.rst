.. _examples_vhost:

=======
 vhost
=======

:Release: |version|
:Date: |today|

.. contents::
    :local:
    :depth: 2

Description
===========

This example project demonstrates how to use a single Redis container as both a broker and a result backend,
using different vhosts for each purpose.

Breakdown
=========

File Structure
~~~~~~~~~~~~~~

The following diagram lists the relevant files in the project.

.. code-block:: text

    rabbitmq_management/
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py
    │   └── test_vhost.py
    └── requirements.txt

conftest.py
~~~~~~~~~~~

We create our own Redis container, and then use it as both a broker and a result backend.

.. code-block:: python

    redis_image = fetch(repository=REDIS_IMAGE)
    redis_test_container: RedisContainer = container(
        image="{redis_image.id}",
        ports=REDIS_PORTS,
        environment=REDIS_ENV,
        network="{default_pytest_celery_network.name}",
        wrapper_class=RedisContainer,
        timeout=REDIS_CONTAINER_TIMEOUT,
    )

As the default vhost is "0", we can use it as the broker, and create a new vhost for the result backend.

.. code-block:: python

    @pytest.fixture
    def redis_broker(redis_test_container: RedisContainer) -> RedisTestBroker:
        broker = RedisTestBroker(redis_test_container)
        yield broker
        broker.teardown()


    @pytest.fixture
    def celery_broker_cluster(redis_broker: RedisTestBroker) -> CeleryBrokerCluster:
        cluster = CeleryBrokerCluster(redis_broker)
        yield cluster
        cluster.teardown()

For the backend, we need to change some settings to use a different vhost, so we create our own
Redis backend and work it out there.

.. code-block:: python

    class MyRedisTestBackend(RedisTestBackend):
        def config(self, *args: tuple, **kwargs: dict) -> dict:
            return super().config(vhost=1, *args, **kwargs)

Lastly, we add our backend that uses the same Redis container as the broker and our
``MyRedisTestBackend`` class.

.. code-block:: python

    @pytest.fixture
    def redis_backend(redis_test_container: RedisContainer) -> MyRedisTestBackend:
        backend = MyRedisTestBackend(redis_test_container)
        yield backend
        backend.teardown()


    @pytest.fixture
    def celery_backend_cluster(redis_backend: MyRedisTestBackend) -> CeleryBackendCluster:
        cluster = CeleryBackendCluster(redis_backend)
        yield cluster
        cluster.teardown()

test_vhost.py
~~~~~~~~~~~~~

We can now run tests that will share the same Redis container for both the broker and the result backend components.

.. literalinclude:: ../../../examples/vhost/tests/test_vhost.py
   :language: python
   :caption: examples.vhost.tests.test_vhost.py
