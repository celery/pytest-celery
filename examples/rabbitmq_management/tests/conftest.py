import pytest

from pytest_celery import RABBITMQ_PORTS
from pytest_celery import CeleryBrokerCluster
from pytest_celery import RabbitMQContainer
from pytest_celery import RabbitMQTestBroker


@pytest.fixture
def default_rabbitmq_broker_image() -> str:
    return "rabbitmq:management"


@pytest.fixture
def default_rabbitmq_broker_ports() -> dict:
    # Expose the management UI port
    ports = RABBITMQ_PORTS.copy()
    ports.update({"15672/tcp": None})
    return ports


class RabbitMQManagementTestBroker(RabbitMQTestBroker):
    def get_management_url(self) -> str:
        ip = self.container.attrs["NetworkSettings"]["Ports"]["15672/tcp"][0]["HostIp"]
        port = self.container.attrs["NetworkSettings"]["Ports"]["15672/tcp"][0]["HostPort"]
        # Opening this link during debugging allows you to see the RabbitMQ management UI
        # in your browser
        return f"http://{ip}:{port}"


@pytest.fixture
def celery_rabbitmq_broker(default_rabbitmq_broker: RabbitMQContainer) -> RabbitMQTestBroker:
    broker = RabbitMQManagementTestBroker(default_rabbitmq_broker)
    yield broker
    broker.teardown()


@pytest.fixture
def celery_broker_cluster(celery_rabbitmq_broker: RabbitMQTestBroker) -> CeleryBrokerCluster:  # type: ignore
    cluster = CeleryBrokerCluster(celery_rabbitmq_broker)  # type: ignore
    yield cluster
    cluster.teardown()
