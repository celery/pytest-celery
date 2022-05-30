from unittest.mock import MagicMock, patch

from testcontainers.rabbitmq import RabbitMqContainer

from pytest_celery.test_services.message_brokers import RabbitMQBroker


def test_rabbitmq_broker_url(test_session_id, subtests):
    with patch.object(RabbitMqContainer, "get_exposed_port") as get_exposed_port_mocked:
        get_exposed_port_mocked.return_value = 5672
        container = RabbitMqContainer()
        broker = RabbitMQBroker(test_session_id, container=container)
        expected_url = "pyampq://guest:guest@localhost:5672"

        with subtests.test("RabbitMQ Broker url"):
            assert broker.url == expected_url

        with subtests.test("Debug representation includes original url in full"):
            assert repr(broker) == f"RabbitMQ Broker <{expected_url}>"


def test_rabbitmq_broker_ping(test_session_id, subtests):
    with patch.object(RabbitMqContainer, "get_exposed_port") as get_exposed_port_mocked:
        get_exposed_port_mocked.return_value = 15672
        container = RabbitMqContainer()
        broker = RabbitMQBroker(test_session_id, container=container)
        with patch("urllib.request") as urllib_request:
            f = MagicMock()
            f.read.return_value = b"""{"status": "ok"}"""
            urllib_request.urlopen.return_value = f
            broker.ping()
            with subtests.test("RabbitMQ Manager aliveness endpoint was tested"):
                urllib_request.urlopen.assert_called_once_with("http://localhost:15672/api/aliveness-test/%2F")
