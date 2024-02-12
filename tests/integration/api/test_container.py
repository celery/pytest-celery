from __future__ import annotations

import pytest

from pytest_celery import CeleryTestContainer
from tests.defaults import ALL_COMPONENTS_FIXTURES


@pytest.fixture
def container(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("container", ALL_COMPONENTS_FIXTURES, indirect=["container"])
class test_celery_test_container:
    def test_client(self, container: CeleryTestContainer):
        assert container.client

    def test_ready(self, container: CeleryTestContainer):
        assert container.ready()
