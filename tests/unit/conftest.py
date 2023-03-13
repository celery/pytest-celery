from pytest_docker_tools import container
from pytest_docker_tools import fetch
from unit.docker.api import UnitTestContainer
from unit.docker.fixtures import unit_tests_container  # noqa
from unit.docker.fixtures import unit_tests_image  # noqa

from pytest_celery import RabbitMQContainer
from pytest_celery import RedisContainer
from pytest_celery import defaults

local_test_container = container(image="{unit_tests_image.id}", wrapper_class=UnitTestContainer)


redis_image = fetch(repository="redis:latest")
redis_test_container = container(
    image="{redis_image.id}",
    scope="session",
    ports={"6379/tcp": None},
    environment={},
    wrapper_class=RedisContainer,
)

rabbitmq_image = fetch(repository="rabbitmq:latest")
rabbitmq_test_container = container(
    image="{rabbitmq_image.id}",
    scope="session",
    ports={"5672/tcp": None},
    environment={},
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)
