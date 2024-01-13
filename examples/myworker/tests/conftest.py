import pytest

from pytest_celery.vendors.rabbitmq.defaults import RABBITMQ_PORTS
from tests.myworker.myworker import myworker_container  # noqa
from tests.myworker.myworker import myworker_image  # noqa
from tests.myworker.myworker import myworker_worker  # noqa


@pytest.fixture
def default_rabbitmq_broker_image() -> str:
    # Useful for debugging
    return "rabbitmq:management"


@pytest.fixture
def default_rabbitmq_broker_ports() -> dict:
    # Expose the management UI port
    ports = RABBITMQ_PORTS.copy()
    ports.update({"15672/tcp": None})
    return ports
