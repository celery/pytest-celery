import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import defaults
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker


@pytest.mark.parametrize(
    "node",
    [
        lazy_fixture(defaults.CELERY_RABBITMQ_BROKER),
    ],
)
class test_rabbitmq_test_broker:
    def test_ready(self, node: RabbitMQTestBroker):
        assert node.ready()
