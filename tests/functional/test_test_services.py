import uuid

import docker
import pytest

from pytest_celery.test_services.message_brokers import RabbitMQBroker, RedisBroker
from pytest_celery.test_services.result_backends import RedisResultBackend


@pytest.mark.parametrize("test_service_cls", [RedisBroker, RedisResultBackend, RabbitMQBroker])
def test_test_service_basic_functionality(test_service_cls, subtests, faker):
    test_session_id = uuid.uuid4()
    test_service = test_service_cls(test_session_id)

    test_service.start()

    docker_container_id = test_service._container.get_wrapped_container().id
    client = docker.from_env()

    with subtests.test("Ensure docker container is running", test_service_cls=test_service_cls.__name__):
        containers = client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 1

    with subtests.test("Ensure test service is responsive", test_service_cls=test_service_cls.__name__):
        test_service.ping()

    test_service.stop()

    with subtests.test("Ensure container is now stopped", test_service_cls=test_service_cls.__name__):
        containers = client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 0


@pytest.mark.parametrize("test_service_cls", [RedisBroker, RedisResultBackend, RabbitMQBroker])
def test_test_service_basic_functionality_context_manager(test_service_cls, subtests, faker):
    test_session_id = uuid.uuid4()
    test_service = test_service_cls(test_session_id)

    with test_service:
        docker_container_id = test_service._container.get_wrapped_container().id
        client = docker.from_env()

        with subtests.test("Ensure docker container is running", test_service_cls=test_service_cls.__name__):
            containers = client.containers.list(filters={"id": docker_container_id})
            assert len(containers) == 1

        with subtests.test("Ensure test service is responsive", test_service_cls=test_service_cls.__name__):
            test_service.ping()

    with subtests.test("Ensure container is now stopped", test_service_cls=test_service_cls.__name__):
        containers = client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 0
