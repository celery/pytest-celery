from unittest.mock import Mock
from unittest.mock import patch

import pytest

from pytest_celery import CeleryWorkerContainer
from pytest_celery import LocalstackContainer
from pytest_celery import MemcachedContainer
from pytest_celery import RabbitMQContainer
from pytest_celery import RedisContainer


@pytest.fixture(autouse=True)
def mock_wait_for_callable():
    with patch("pytest_celery.api.base.wait_for_callable", new=Mock()):
        with patch("pytest_celery.api.container.wait_for_callable", new=Mock()):
            yield


def mocked_container(spec: type) -> Mock:
    mocked_container = Mock(spec=spec)
    mocked_container.id = "mocked_test_container_id"
    mocked_container.celeryconfig = {
        "url": "mocked_url/",
        "host_url": "mocked_host_url/",
    }
    return mocked_container


@pytest.fixture
def default_localstack_broker() -> LocalstackContainer:
    return mocked_container(LocalstackContainer)


@pytest.fixture
def default_memcached_backend() -> MemcachedContainer:
    return mocked_container(MemcachedContainer)


@pytest.fixture
def default_rabbitmq_broker() -> RabbitMQContainer:
    return mocked_container(RabbitMQContainer)


@pytest.fixture
def default_redis_backend() -> RedisContainer:
    return mocked_container(RedisContainer)


@pytest.fixture
def default_redis_broker() -> RedisContainer:
    return mocked_container(RedisContainer)


@pytest.fixture
def default_worker_container() -> CeleryWorkerContainer:
    return mocked_container(CeleryWorkerContainer)
