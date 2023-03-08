import pytest

from pytest_celery import defaults
from pytest_celery.api.setup import CeleryTestSetup
from pytest_celery.components.backend.redis.api import RedisTestBackend
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker


@pytest.mark.parametrize("i", list(range(1)))
def test_celery_setup(celery_setup: CeleryTestSetup, i):
    celery_setup.ready()
    assert celery_setup.ready()


def test_multi_setup(celery_multi_setup: CeleryTestSetup):
    celery_multi_setup.ready()
    assert celery_multi_setup.ready()


@pytest.mark.parametrize("i", list(range(1)))
def test_all_celery_components(celery_session_broker, celery_session_backend, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_all_brokers_vs_rabbit(celery_session_broker, celery_rabbitmq_broker, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_all_brokers_vs_redis(celery_session_broker, celery_redis_broker, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_all_backends_vs_rabbit(celery_session_backend, celery_rabbitmq_broker, i):
    pass


@pytest.mark.parametrize("i", list(range(1)))
def test_rabbitmq_broker_redis_backend(
    celery_rabbitmq_broker: RabbitMQTestBroker, celery_redis_backend: RedisTestBackend, i
):
    assert defaults.REDIS_IMAGE == celery_redis_backend.container.attrs["Config"]["Image"]
    assert defaults.RABBITMQ_IMAGE == celery_rabbitmq_broker.container.attrs["Config"]["Image"]
