from unittest.mock import patch

import pytest
from celery.exceptions import Ignore

from pytest_celery import add
from pytest_celery import add_replaced
from pytest_celery import fail
from pytest_celery import identity
from pytest_celery import noop
from pytest_celery import ping
from pytest_celery import sleep
from pytest_celery import xsum


class test_default_tasks:
    def test_add(self):
        assert add(1, 2) == 3

    def test_add_replaced(self):
        with patch("pytest_celery.add_replaced.replace", side_effect=Ignore):
            with pytest.raises(Ignore):
                add_replaced(1, 2)

    def test_fail(self):
        with pytest.raises(RuntimeError):
            fail()

    def test_identity(self):
        assert identity(1) == 1

    def test_noop(self):
        assert noop() is None

    def test_ping(self):
        assert ping() == "pong"

    def test_sleep(self):
        assert sleep() is True

    def test_xsum(self):
        assert xsum([1, 2, 3]) == 6

    def test_xsum_nested_list(self):
        assert xsum([[1, 2], [3, 4], [5, 6]]) == 21
