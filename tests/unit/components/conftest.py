import pytest

from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker
from pytest_celery import RedisContainer
from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker


@pytest.fixture
def celery_redis_backend(redis_test_container: RedisContainer) -> RedisTestBackend:
    return RedisTestBackend(redis_test_container)


@pytest.fixture
def celery_redis_broker(redis_test_container: RedisContainer) -> RedisTestBroker:
    return RedisTestBroker(redis_test_container)


@pytest.fixture
def celery_rabbitmq_broker(rabbitmq_test_container: RabbitMQContainer) -> RabbitMQTestBroker:
    return RabbitMQTestBroker(rabbitmq_test_container)
