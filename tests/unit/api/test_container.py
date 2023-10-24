from unittest.mock import Mock

import pytest

from pytest_celery import CeleryTestContainer


@pytest.fixture
def mocked_container() -> CeleryTestContainer:
    docker_container_mock = Mock()
    return CeleryTestContainer(container=docker_container_mock)


class test_celery_test_container:
    def test_client(self, mocked_container: CeleryTestContainer):
        with pytest.raises(NotImplementedError):
            mocked_container.client
