import pytest

from pytest_celery.markers import MessageBroker


@pytest.mark.messagebroker(MessageBroker.RabbitMQ)
def test_successful_when_message_broker_quantity_is_1():
    # should result in 1 passed test
    pass


@pytest.mark.messagebroker(MessageBroker.RabbitMQ)
@pytest.mark.messagebroker(MessageBroker.Redis)
def test_successful_when_message_broker_quantity_is_2():
    # should result in 2 passed tests
    pass


@pytest.mark.messagebroker(MessageBroker.RabbitMQ)
@pytest.mark.messagebroker(MessageBroker.RabbitMQ)
def test_raises_error_when_message_broker_is_duplicated_without_configuration():
    # should use messagebroker(MessageBroker.RabbitMQ, n=2) instead
    # error should clarify that
    pass
