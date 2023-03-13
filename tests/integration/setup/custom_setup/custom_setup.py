import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryBrokerCluster
from pytest_celery import CeleryTestSetup
from pytest_celery import RabbitMQContainer
from pytest_celery import RedisContainer

main_redis_backend = container(
    image="{redis_function_backend_image}",
    ports=fxtr("redis_function_backend_ports"),
    environment=fxtr("redis_function_backend_env"),
    wrapper_class=RedisContainer,
)

alt_redis_backend = container(
    image="{alt_redis_backend_image}",
    ports=fxtr("alt_redis_backend_ports"),
    environment=fxtr("alt_redis_backend_env"),
    wrapper_class=RedisContainer,
)


@pytest.fixture
def alt_redis_backend_env(redis_function_backend_env):
    return redis_function_backend_env


@pytest.fixture
def alt_redis_backend_image(redis_function_backend_image):
    return redis_function_backend_image


@pytest.fixture
def alt_redis_backend_ports(redis_function_backend_ports):
    return redis_function_backend_ports


main_redis_broker = container(
    image="{redis_function_broker_image}",
    ports=fxtr("redis_function_broker_ports"),
    environment=fxtr("redis_function_broker_env"),
    wrapper_class=RedisContainer,
)

main_rabbitmq_broker = container(
    image="{rabbitmq_function_broker_image}",
    ports=fxtr("rabbitmq_function_broker_ports"),
    environment=fxtr("rabbitmq_function_broker_env"),
    wrapper_class=RabbitMQContainer,
)

alt_rabbitmq_broker = container(
    image="{alt_rabbitmq_broker_image}",
    ports=fxtr("alt_rabbitmq_broker_ports"),
    environment=fxtr("alt_rabbitmq_broker_env"),
    wrapper_class=RabbitMQContainer,
)


@pytest.fixture
def alt_rabbitmq_broker_env(rabbitmq_function_broker_env):
    return rabbitmq_function_broker_env


@pytest.fixture
def alt_rabbitmq_broker_image(rabbitmq_function_broker_image):
    return rabbitmq_function_broker_image


@pytest.fixture
def alt_rabbitmq_broker_ports(rabbitmq_function_broker_ports):
    return rabbitmq_function_broker_ports


@pytest.fixture
def my_backend_cluster(main_redis_backend, alt_redis_backend):
    return CeleryBackendCluster(main_redis_backend, alt_redis_backend)


@pytest.fixture
def my_broker_cluster(main_redis_broker, main_rabbitmq_broker, alt_rabbitmq_broker):
    return CeleryBrokerCluster(main_redis_broker, main_rabbitmq_broker, alt_rabbitmq_broker)


@pytest.fixture
def my_custom_setup(my_backend_cluster, my_broker_cluster):
    setup = CeleryTestSetup(my_backend_cluster, my_broker_cluster)
    setup.ready()
    return setup
