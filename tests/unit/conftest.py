import pytest
from celery import Celery
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fetch
from pytest_docker_tools import fxtr
from pytest_docker_tools import network
from pytest_docker_tools import volume

from pytest_celery import defaults
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.components.backend.redis.api import RedisTestBackend
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.components.broker.redis.api import RedisTestBroker
from pytest_celery.containers.rabbitmq import RabbitMQContainer
from pytest_celery.containers.redis import RedisContainer
from pytest_celery.containers.worker import CeleryWorkerContainer
from tests.unit.docker.api import UnitTestContainer

unit_tests_network = network(scope="session")

unit_tests_image = build(
    path="tests/unit/docker",
    tag="pytest-celery/tests/unit:latest",
)

unit_tests_container = container(
    image="{unit_tests_image.id}",
    scope="session",
    network="{unit_tests_network.name}",
    wrapper_class=UnitTestContainer,
)

local_test_container = container(
    image="{unit_tests_image.id}",
    network="{unit_tests_network.name}",
    wrapper_class=UnitTestContainer,
)

celery_unit_worker_image = build(
    path="src/pytest_celery/components/worker",
    tag="pytest-celery/components/worker:unit",
    buildargs={
        "CELERY_VERSION": fxtr("default_worker_celery_version"),
    },
)

worker_test_container_volume = volume(
    initial_content=fxtr("worker_test_container_initial_content"),
    scope="session",
)


@pytest.fixture(scope="session")
def worker_test_container_initial_content(worker_test_container_tasks: set) -> dict:
    return CeleryWorkerContainer.initial_content(worker_test_container_tasks)


@pytest.fixture(scope="session")
def worker_test_container_tasks() -> set:
    return CeleryWorkerContainer.tasks_modules()


worker_test_container = container(
    image="{celery_unit_worker_image.id}",
    scope="session",
    environment=defaults.DEFAULT_WORKER_ENV,
    network="{unit_tests_network.name}",
    volumes={"{worker_test_container_volume.name}": {"bind": "/app", "mode": "rw"}},
    wrapper_class=CeleryWorkerContainer,
    timeout=defaults.DEFAULT_WORKER_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_test_worker(worker_test_container: CeleryWorkerContainer, celery_setup_app: Celery) -> CeleryTestWorker:
    return CeleryTestWorker(
        container=worker_test_container,
        app=celery_setup_app,
    )


redis_image = fetch(repository=defaults.REDIS_IMAGE)
redis_test_container = container(
    image="{redis_image.id}",
    scope="session",
    ports=defaults.REDIS_PORTS,
    environment=defaults.REDIS_ENV,
    network="{unit_tests_network.name}",
    wrapper_class=RedisContainer,
    timeout=defaults.REDIS_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_redis_backend(redis_test_container: RedisContainer) -> RedisTestBackend:
    return RedisTestBackend(redis_test_container)


@pytest.fixture
def celery_redis_broker(redis_test_container: RedisContainer) -> RedisTestBroker:
    return RedisTestBroker(redis_test_container)


rabbitmq_image = fetch(repository=defaults.RABBITMQ_IMAGE)
rabbitmq_test_container = container(
    image="{rabbitmq_image.id}",
    scope="session",
    ports=defaults.RABBITMQ_PORTS,
    environment=defaults.RABBITMQ_ENV,
    network="{unit_tests_network.name}",
    wrapper_class=RabbitMQContainer,
    timeout=defaults.RABBITMQ_CONTAINER_TIMEOUT,
)


@pytest.fixture
def celery_rabbitmq_broker(rabbitmq_test_container: RabbitMQContainer) -> RabbitMQTestBroker:
    return RabbitMQTestBroker(rabbitmq_test_container)
