import pytest

from pytest_celery.test_services.message_brokers import RabbitMQBroker


@pytest.mark.parametrize("test_service_cls", [RabbitMQBroker])
def test_ping(test_service_cls, faker):
    test_session_id = faker.uuid4()
    test_service = test_service_cls(test_session_id)
    with test_service:
        test_service.ping()
        connection = test_service.get_client
        channel = connection.channel()
        _, _, body = channel.basic_get("ping")
        assert body == b'PING'
