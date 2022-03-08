from unittest.mock import Mock

import pytest
from testcontainers.redis import RedisContainer

from pytest_celery.test_services.message_brokers import RedisBroker


@pytest.fixture
def redis_container_mock() -> Mock:
    return Mock(spec_set=RedisContainer)


@pytest.fixture
def redis_broker(redis_container_mock) -> RedisBroker:
    redis_broker = RedisBroker(redis_container_mock)
    return redis_broker


def test_redis_client(redis_broker: RedisBroker, redis_container_mock):
    redis_broker.start()
    redis_broker.client()

    redis_container_mock.get_client().assert_called_once_with()


def test_ping(redis_broker: RedisBroker, redis_container_mock) -> None:
    redis_broker.ping()

    redis_broker.client.ping.assert_called_once_with()

