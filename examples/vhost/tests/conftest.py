import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fetch

from pytest_celery import REDIS_CONTAINER_TIMEOUT
from pytest_celery import REDIS_ENV
from pytest_celery import REDIS_IMAGE
from pytest_celery import REDIS_PORTS
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryBrokerCluster
from pytest_celery import RedisContainer
from pytest_celery import RedisTestBackend
from pytest_celery import RedisTestBroker

redis_image = fetch(repository=REDIS_IMAGE)
redis_test_container: RedisContainer = container(
    image="{redis_image.id}",
    ports=REDIS_PORTS,
    environment=REDIS_ENV,
    network="{default_pytest_celery_network.name}",
    wrapper_class=RedisContainer,
    timeout=REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def redis_broker(redis_test_container: RedisContainer) -> RedisTestBroker:
    broker = RedisTestBroker(redis_test_container)
    yield broker
    broker.teardown()


@pytest.fixture
def celery_broker_cluster(redis_broker: RedisTestBroker) -> CeleryBrokerCluster:
    cluster = CeleryBrokerCluster(redis_broker)
    yield cluster
    cluster.teardown()


class MyRedisTestBackend(RedisTestBackend):
    def config(self, *args: tuple, **kwargs: dict) -> dict:
        return super().config(vhost=1, *args, **kwargs)


@pytest.fixture
def redis_backend(redis_test_container: RedisContainer) -> MyRedisTestBackend:
    backend = MyRedisTestBackend(redis_test_container)
    yield backend
    backend.teardown()


@pytest.fixture
def celery_backend_cluster(redis_backend: MyRedisTestBackend) -> CeleryBackendCluster:
    cluster = CeleryBackendCluster(redis_backend)
    yield cluster
    cluster.teardown()
