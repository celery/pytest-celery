import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import RabbitMQContainer
from pytest_celery import defaults


@pytest.mark.parametrize("container", lazy_fixture(defaults.ALL_RABBITMQ_FIXTURES))
class test_rabbitmq_container:
    def test_client(self, container: RabbitMQContainer):
        assert container.client()
