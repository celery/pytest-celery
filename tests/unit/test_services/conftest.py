from unittest.mock import Mock, sentinel

import pytest


@pytest.fixture
def container() -> Mock:
    m = Mock()
    m.with_name.return_value = m

    return m


@pytest.fixture
def test_session_id() -> sentinel:
    return sentinel.TEST_SESSION_ID
