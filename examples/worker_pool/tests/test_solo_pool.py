from __future__ import annotations

import pytest
from celery.canvas import Signature
from celery.result import AsyncResult

from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from pytest_celery import ping


class SoloPoolWorker(CeleryWorkerContainer):
    @classmethod
    def command(cls, *args: str) -> list[str]:
        return super().command("-P", "solo")


@pytest.fixture
def default_worker_container_cls() -> type[CeleryWorkerContainer]:
    return SoloPoolWorker


@pytest.fixture(scope="session")
def default_worker_container_session_cls() -> type[CeleryWorkerContainer]:
    return SoloPoolWorker


class TestSoloPool:
    def test_celery_banner(self, celery_worker: CeleryTestWorker):
        celery_worker.assert_log_exists("solo")

    def test_ping(self, celery_setup: CeleryTestSetup):
        sig: Signature = ping.s()
        res: AsyncResult = sig.apply_async()
        assert res.get(timeout=RESULT_TIMEOUT) == "pong"
