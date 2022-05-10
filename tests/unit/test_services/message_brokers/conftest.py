from unittest.mock import Mock

import pytest


@pytest.fixture
def container() -> Mock:
    m = Mock()
    m.with_name.return_value = m

    return m
