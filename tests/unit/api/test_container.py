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

    def test_celeryconfig(self, mocked_container: CeleryTestContainer):
        with pytest.raises(NotImplementedError):
            mocked_container.celeryconfig

    def test_command(self, mocked_container: CeleryTestContainer):
        with pytest.raises(NotImplementedError):
            mocked_container.command()

    def test_teardown(self, mocked_container: CeleryTestContainer):
        mocked_container.teardown()

    def test_ready_prompt(self, mocked_container: CeleryTestContainer):
        assert mocked_container.ready_prompt is None

    def test_wait_port(self, mocked_container: CeleryTestContainer):
        with pytest.raises(ValueError):
            mocked_container._wait_port(None)

    def test_wait_ready(self, mocked_container: CeleryTestContainer):
        assert mocked_container._wait_ready()
