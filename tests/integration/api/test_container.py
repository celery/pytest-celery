import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CeleryTestContainer
from tests.defaults import ALL_COMPONENTS_FIXTURES


@pytest.mark.parametrize("container", lazy_fixture(ALL_COMPONENTS_FIXTURES))
class test_celery_test_container:
    def test_client(self, container: CeleryTestContainer):
        assert container.client

    def test_ready(self, container: CeleryTestContainer):
        assert container.ready()
