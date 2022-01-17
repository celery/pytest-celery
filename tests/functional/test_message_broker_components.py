import docker
import pytest

from pytest_celery.message_brokers.redis_broker import RedisBroker


@pytest.mark.parametrize("message_broker_cls", [RedisBroker])
def test_message_broker_basic_functionality(message_broker_cls, subtests):
    message_broker = message_broker_cls()

    message_broker.start()
    client = docker.from_env()

    with subtests.test("Ensure docker container is running", message_broker_cls=message_broker_cls):
        containers = client.containers.list()

        assert len(containers) == 1

    with subtests.test("Ensure message broker is responsive", message_broker_cls=message_broker_cls):
        message_broker.client.ping()

    message_broker.stop()

    with subtests.test("Ensure container is now stopped", message_broker_cls=message_broker_cls):
        containers = client.containers.list()
        assert len(containers) == 0
