.. _examples_rabbitmq-management:

=====================
 rabbitmq_management
=====================

.. contents::
    :local:
    :depth: 2

Description
===========

This example project demonstrates how to reconfigure the default rabbitmq broker
to use the `rabbitmq:management <https://hub.docker.com/_/rabbitmq>`_ image.
This is very useful for debugging the broker during development but is not recommended
for production use unless you know what you're doing.

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
    │   └── test_management_broker.py
    └── requirements.txt

conftest.py
~~~~~~~~~~~

To reconfigure the default rabbitmq broker container, we override the following
fixtures with our desired values.

First, let's pick our docker image label.

.. code-block:: python

    @pytest.fixture
    def default_rabbitmq_broker_image() -> str:
        return "rabbitmq:management"

Then, we need to expose the management UI port.

.. code-block:: python

    @pytest.fixture
    def default_rabbitmq_broker_ports() -> dict:
        # Expose the management UI port
        ports = RABBITMQ_PORTS.copy()
        ports.update({"15672/tcp": None})
        return ports

The :class:`RabbitMQTestBroker <pytest_celery.vendors.rabbitmq.api.RabbitMQTestBroker>` class is used to represent a logical broker in the
testing environment, so we create our own subclass to represent the management
broker. We add our custom logic to get the REST API URL, which we can later on
access from our tests automatically.

.. code-block:: python

    class RabbitMQManagementTestBroker(RabbitMQTestBroker):
        def get_management_url(self) -> str:
            ip = self.container.attrs["NetworkSettings"]["Ports"]["15672/tcp"][0]["HostIp"]
            port = self.container.attrs["NetworkSettings"]["Ports"]["15672/tcp"][0]["HostPort"]
            return f"http://{ip}:{port}"

We need to override the rabbitmq broker fixture to apply our custom class.
This allows us to extend the broker API with our own implementation.

.. code-block:: python

    @pytest.fixture
    def celery_rabbitmq_broker(default_rabbitmq_broker: RabbitMQContainer) -> RabbitMQTestBroker:
        broker = RabbitMQManagementTestBroker(default_rabbitmq_broker)
        yield broker
        broker.teardown()

The :func:`celery_broker <pytest_celery.fixtures.broker.celery_broker>` fixture is a special parameterized fixture that
provides all of the available broker fixtures. By default :func:`celery_broker_cluster <pytest_celery.fixtures.broker.celery_broker_cluster>`
uses ``celery_broker``. For the sake of the example, we've overridden it to use only one broker, our own custom rabbitmq management broker.

.. code-block:: python

    @pytest.fixture
    def celery_broker_cluster(celery_rabbitmq_broker: RabbitMQTestBroker) -> CeleryBrokerCluster:
        cluster = CeleryBrokerCluster(celery_rabbitmq_broker)
        yield cluster
        cluster.teardown()

test_management_broker.py
~~~~~~~~~~~~~~~~~~~~~~~~~

In the first test, we don't even load a full setup, we just use the broker alone using the default fixture.
We test that we can access the management API using the default credentials.

.. code-block:: python

    def test_login_to_broker_alone(celery_rabbitmq_broker: RabbitMQManagementTestBroker):
        api = celery_rabbitmq_broker.get_management_url() + "/api/whoami"
        response = requests.get(api, auth=HTTPBasicAuth("guest", "guest"))
        assert response.status_code == 200
        assert response.json()["name"] == "guest"
        assert response.json()["tags"] == ["administrator"]

.. note::
    Calling `celery_rabbitmq_broker.get_management_url()` during debug and opening the link in your browser allows you to see the RabbitMQ management UI
    for the tested broker.

In the second test, we load a full setup, and test that the broker is indeed the one we configured.

.. code-block:: python

    def test_broker_in_setup(celery_setup: CeleryTestSetup):
        assert isinstance(celery_setup.broker, RabbitMQManagementTestBroker)
        api = celery_setup.broker.get_management_url() + "/api/queues"
        response = requests.get(api, auth=HTTPBasicAuth("guest", "guest"))
        assert response.status_code == 200
        res = response.json()
        assert isinstance(res, list)
        assert len(list(filter(lambda queues: celery_setup.worker.hostname() in queues["name"], res))) == 1
