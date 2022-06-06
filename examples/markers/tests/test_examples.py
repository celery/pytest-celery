import pytest

from pytest_celery.test_services.message_brokers import RedisBroker, RabbitMQBroker
from pytest_celery.test_services.result_backends import RedisResultBackend, RabbitMQResultBackend
from pytest_celery.contrib.testing.tasks import ping

TIMEOUT = 60


@pytest.mark.messagebroker.with_args(RedisBroker)
@pytest.mark.resultbackend.with_args(RedisResultBackend)
def test_successful_when_message_broker_quantity_is_1(message_broker, result_backend):
    print("hello")
    print(message_broker.url)


# @pytest.mark.messagebroker.with_args(RedisBroker)
# @pytest.mark.resultbackend.with_args(RedisResultBackend)
# @pytest.mark.resultbackend.with_args(RabbitMQResultBackend)
# @pytest.mark.messagebroker.with_args(RabbitMQBroker)
# @pytest.mark.celery
# def test_task(message_broker, result_backend, manager):
#     """
#     Test that a simple group completes.
#     """
#     sig = ping.s()
#     res = sig.delay()
#     assert res.get(timeout=TIMEOUT) == "pong"
