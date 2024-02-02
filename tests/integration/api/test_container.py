from __future__ import annotations

import pytest

from pytest_celery import CeleryTestContainer
from tests.defaults import ALL_COMPONENTS_FIXTURES


@pytest.mark.parametrize("container", ALL_COMPONENTS_FIXTURES)
class test_celery_test_container:
    def test_client(self, container: CeleryTestContainer, request):
        container = request.getfixturevalue(container)
        assert container.client

    def test_ready(self, container: CeleryTestContainer, request):
        container = request.getfixturevalue(container)
        assert container.ready()
