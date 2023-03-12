import pytest
from integration.setup.custom_setup.custom_setup import *  # noqa

from pytest_celery.api.setup import CeleryTestSetup


@pytest.fixture
def celery_setup(my_custom_setup: CeleryTestSetup) -> CeleryTestSetup:
    return my_custom_setup
