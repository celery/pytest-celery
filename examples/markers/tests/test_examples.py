
import pytest

from pytest_celery.test_services.message_brokers import RedisBroker
from pytest_celery.test_services.result_backends import RedisResultBackend


@pytest.mark.messagebroker.with_args(RedisBroker)
@pytest.mark.resultbackend.with_args(RedisResultBackend)
def test_successful_when_message_broker_quantity_is_1(message_broker, result_backend):
    pass