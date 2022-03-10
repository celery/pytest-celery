from __future__ import annotations

from unittest.mock import Mock

import pytest

from pytest_celery.test_services import TestService


class FakeTestService(TestService):
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    @property
    def url(self):
        pass

    def to_node(self):
        pass


@pytest.fixture
def container() -> Mock:
    return Mock()


@pytest.fixture
def test_session_id(faker):
    return str(faker.uuid4())


def test_initialization(container, test_session_id, subtests):
    test_service = FakeTestService(container, test_session_id)

    with subtests.test("Service is intialized"):
        assert test_service._container == container.with_name("bla")
        assert test_service.test_session_id == test_session_id

    with subtests.test("Container received name"):
        assert test_service.name == "bla"

