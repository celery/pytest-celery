import pytest
from celery import group

from pytest_celery.test_services.message_brokers import RedisBroker
from pytest_celery.test_services.result_backends import RedisResultBackend
from tests.tasks import identity

TIMEOUT = 60


@pytest.mark.messagebroker.with_args(RedisBroker)
@pytest.mark.resultbackend.with_args(RedisResultBackend)
def test_successful_when_message_broker_quantity_is_1(message_broker, result_backend, app):
    print("hello")
    print(app)
    print(message_broker.url)


@pytest.mark.messagebroker.with_args(RedisBroker)
@pytest.mark.resultbackend.with_args(RedisResultBackend)
@pytest.mark.celery
def test_task(message_broker, result_backend, app):
    """
    Test that a simple group completes.
    """
    print("app", app)
    sig = identity.s(42)
    res = sig.delay()
    assert res.get(timeout=TIMEOUT) == 42
