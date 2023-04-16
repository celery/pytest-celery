import pytest

from pytest_celery import CeleryTestContainer
from pytest_celery import defaults
from pytest_celery.utils import resilient_lazy_fixture as lazy_fixture


@pytest.mark.parametrize("container", lazy_fixture(defaults.ALL_COMPONENTS_FIXTURES))
class test_celery_test_container:
    def test_client(self, container: CeleryTestContainer):
        assert container.client
