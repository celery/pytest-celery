import uuid

import docker
import pytest

from pytest_celery.test_services.message_brokers import KafkaBroker, RabbitMQBroker, RedisBroker
from pytest_celery.test_services.result_backends import RabbitMQResultBackend, RedisResultBackend


@pytest.fixture
def test_session_id(faker):
    return uuid.uuid4()


@pytest.fixture(params=(RedisBroker, RedisResultBackend, RabbitMQBroker, RabbitMQResultBackend, KafkaBroker))
def test_service(request, test_session_id):
    return request.param(test_session_id)


@pytest.fixture
def test_service_name(test_service):
    return test_service.__class__.__name__


@pytest.fixture(scope="session")
def docker_client():
    return docker.from_env()


def get_docker_container_id(test_service):
    return test_service._container.get_wrapped_container().id


def test_test_service_basic_functionality(test_service, test_service_name, docker_client, subtests):
    test_service.start()
    docker_container_id = get_docker_container_id(test_service)

    with subtests.test("Ensure docker container is running", test_service_cls=test_service_name):
        containers = docker_client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 1

    with subtests.test("Ensure test service is responsive", test_service_cls=test_service_name):
        test_service.ping()

    with subtests.test("Ensure container is now stopped", test_service_cls=test_service_name):
        test_service.stop()

        containers = docker_client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 0


def test_test_service_basic_functionality_context_manager(test_service, test_service_name, docker_client, subtests):
    with test_service:
        docker_container_id = get_docker_container_id(test_service)

        with subtests.test("Ensure docker container is running", test_service_cls=test_service_name):
            containers = docker_client.containers.list(filters={"id": docker_container_id})
            assert len(containers) == 1

        with subtests.test("Ensure test service is responsive", test_service_cls=test_service_name):
            test_service.ping()

    with subtests.test("Ensure container is now stopped", test_service_cls=test_service_name):
        containers = docker_client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 0
