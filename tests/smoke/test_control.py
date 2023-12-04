from __future__ import annotations

from pytest_celery import CeleryTestSetup


class test_control:
    def test_control_ping(self, celery_setup: CeleryTestSetup):
        r = celery_setup.app.control.ping()
        assert all([all([res["ok"] == "pong" for _, res in response.items()]) for response in r])
