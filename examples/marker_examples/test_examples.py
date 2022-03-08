import pytest

from pytest_celery.test_services.message_brokers import RedisBroker


@pytest.mark.messagebroker.with_args(RedisBroker)
def test_successful_when_message_broker_quantity_is_1(message_broker):
    # should result in 1 passed test
    pass


# @pytest.mark.messagebroker(RedisBroker)
# # @pytest.mark.messagebroker(RabbitMQBroker)
# def test_successful_when_message_broker_quantity_is_2():
#     # should result in 2 passed tests
#     pass
#


@pytest.mark.messagebroker.with_args(RedisBroker)
@pytest.mark.messagebroker.with_args(RedisBroker)
def test_raises_error_when_message_broker_is_duplicated_without_configuration(message_broker):
    # should use messagebroker(RedisBroker, n=2) instead
    # error should clarify that
    pass
