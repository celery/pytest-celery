from unittest.mock import MagicMock, patch

import pytest
from testcontainers.rabbitmq import RabbitMqContainer

from pytest_celery.test_services.message_brokers import RabbitMQBroker
from pytest_celery.test_services.result_backends import RabbitMQResultBackend


@pytest.mark.parametrize("test_service,url,representation",
                         [(RabbitMQBroker, "pyampq://guest:guest@localhost:5672",
                           "RabbitMQ Broker <pyampq://guest:guest@localhost:5672>"),
                          (RabbitMQResultBackend, "rpc://guest:guest@localhost:5672",
                           "RabbitMQ Result Backend <rpc://guest:guest@localhost:5672>")])
def test_rabbitmq_url(test_session_id, subtests, test_service, url, representation):
    with patch.object(RabbitMqContainer, "get_exposed_port") as get_exposed_port_mocked:
        get_exposed_port_mocked.return_value = 5672
        container = RabbitMqContainer()
        service = test_service(test_session_id, container=container)

        with subtests.test("RabbitMQ Broker url"):
            assert service.url == url

        with subtests.test("Debug representation includes original url in full"):
            assert repr(service) == representation


@pytest.mark.parametrize("test_service", [RabbitMQBroker, RabbitMQResultBackend])
def test_rabbitmq_broker_ping(test_session_id, subtests, test_service):
    with patch.object(RabbitMqContainer, "get_exposed_port") as get_exposed_port_mocked:
        get_exposed_port_mocked.return_value = 15672
        container = RabbitMqContainer()
        broker = test_service(test_session_id, container=container)
        with patch("urllib.request") as urllib_request:
            f = MagicMock()
            f.read.return_value = b"""{"status": "ok"}"""
            urllib_request.urlopen.return_value = f
            broker.ping()
            with subtests.test("RabbitMQ Manager aliveness endpoint was tested"):
                urllib_request.urlopen.assert_called_once_with("http://localhost:15672/api/aliveness-test/%2F")
