import docker
import pytest

from pytest_celery.test_services.message_brokers import RedisBroker


@pytest.mark.parametrize("message_broker_cls", [RedisBroker])
def test_message_broker_basic_functionality(message_broker_cls, subtests, faker):
    message_broker = message_broker_cls(faker.uuid4())

    message_broker.start()

    docker_container_id = message_broker._container.get_wrapped_container().id
    client = docker.from_env()

    with subtests.test("Ensure docker container is running", message_broker_cls=message_broker_cls):
        containers = client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 1

    with subtests.test("Ensure message broker is responsive", message_broker_cls=message_broker_cls):
        message_broker.ping()

    message_broker.stop()

    with subtests.test("Ensure container is now stopped", message_broker_cls=message_broker_cls):
        containers = client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 0


@pytest.mark.parametrize("message_broker_cls", [RedisBroker])
def test_message_broker_basic_functionality_context_manager(message_broker_cls, subtests, faker):
    message_broker = message_broker_cls(faker.uuid4())

    with message_broker:
        docker_container_id = message_broker._container.get_wrapped_container().id
        client = docker.from_env()

        with subtests.test("Ensure docker container is running", message_broker_cls=message_broker_cls):
            containers = client.containers.list(filters={"id": docker_container_id})
            assert len(containers) == 1

        with subtests.test("Ensure message broker is responsive", message_broker_cls=message_broker_cls):
            message_broker.ping()

    with subtests.test("Ensure container is now stopped", message_broker_cls=message_broker_cls):
        containers = client.containers.list(filters={"id": docker_container_id})
        assert len(containers) == 0
