import pytest

from pytest_celery import RabbitMQTestBroker
from pytest_celery import defaults
from pytest_celery.utils import resilient_lazy_fixture as lazy_fixture


@pytest.mark.parametrize("node", [lazy_fixture(defaults.CELERY_RABBITMQ_BROKER)])
class test_rabbitmq_test_broker:
    def test_ready(self, node: RabbitMQTestBroker):
        assert node.ready()
