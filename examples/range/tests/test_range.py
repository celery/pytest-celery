import pytest
from celery.canvas import Signature
from celery.result import AsyncResult

from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryTestSetup
from pytest_celery import ping
from tests.conftest import get_celery_versions


class TestRange:
    @pytest.fixture(scope="session", params=get_celery_versions("v4.4.7", "v5.0.0"))
    def default_worker_celery_version(self, request: pytest.FixtureRequest) -> str:
        return request.param

    def test_ping(self, celery_setup: CeleryTestSetup, default_worker_celery_version: str):
        sig: Signature = ping.s()
        res: AsyncResult = sig.apply_async()
        assert res.get(timeout=RESULT_TIMEOUT) == "pong"
