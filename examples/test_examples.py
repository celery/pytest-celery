import pytest

from pytest_celery.message_brokers.redis_broker import RedisBroker


@pytest.mark.messagebroker(RedisBroker)
def test_successful_when_message_broker_quantity_is_1():
    # should result in 1 passed test
    pass


# @pytest.mark.messagebroker(RedisBroker)
# @pytest.mark.messagebroker(RabbitMQBroker)
# def test_successful_when_message_broker_quantity_is_2():
#     # should result in 2 passed tests
#     pass


@pytest.mark.messagebroker(RedisBroker)
@pytest.mark.messagebroker(RedisBroker)
def test_raises_error_when_message_broker_is_duplicated_without_configuration():
    # should use messagebroker(RedisBroker, n=2) instead
    # error should clarify that
    pass
