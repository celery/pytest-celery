from __future__ import annotations

import pytest

from pytest_celery import CeleryTestSetup


@pytest.mark.parametrize(
    "pool",
    [
        "solo",
        "prefork",
        "threads",
    ],
)
class test_replacing_pool:
    @pytest.fixture
    def default_worker_command(self, default_worker_command: list[str], pool: str) -> list[str]:
        return [*default_worker_command, "--pool", pool]

    def test_pool_from_celery_banner(self, celery_setup: CeleryTestSetup, pool: str):
        if pool == "threads":
            pool = "thread"
        celery_setup.worker.assert_log_exists(pool)
