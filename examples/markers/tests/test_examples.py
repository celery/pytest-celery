import pytest

from pytest_celery.contrib.testing.tasks import ping
from pytest_celery.test_services.message_brokers import RabbitMQBroker, RedisBroker
from pytest_celery.test_services.result_backends import RabbitMQResultBackend, RedisResultBackend

TIMEOUT = 60


@pytest.mark.messagebroker.with_args(RedisBroker)
@pytest.mark.resultbackend.with_args(RedisResultBackend)
def test_successful_when_message_broker_quantity_is_1(message_broker, result_backend):
    print(message_broker.url)
    print(result_backend.url)


@pytest.mark.messagebroker.with_args(RedisBroker)
@pytest.mark.messagebroker.with_args(RabbitMQBroker)
@pytest.mark.resultbackend.with_args(RedisResultBackend)
@pytest.mark.resultbackend.with_args(RabbitMQResultBackend)
@pytest.mark.celery
def test_simple_task(message_broker, result_backend, manager):
    sig = ping.s()
    res = sig.delay()
    assert res.get(timeout=TIMEOUT) == "pong"
