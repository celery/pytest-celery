import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import defaults
from pytest_celery.components.containers.redis import RedisContainer


@pytest.mark.parametrize(
    "container",
    lazy_fixture(defaults.ALL_REDIS_FIXTURES),
)
class test_redis_container:
    def test_client(self, container: RedisContainer):
        assert container.client()
