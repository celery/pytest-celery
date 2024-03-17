from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryTestSetup
from pytest_celery import ping


class TestVhost:
    def test_ping(self, celery_setup: CeleryTestSetup):
        assert ping.s().delay().get(timeout=RESULT_TIMEOUT) == "pong"

    def test_vhost(self, celery_setup: CeleryTestSetup):
        assert celery_setup.app.conf.broker_url[:-1] == celery_setup.app.conf.result_backend[:-1]
        assert celery_setup.app.conf.broker_url.endswith("/0")
        assert celery_setup.app.conf.result_backend.endswith("/1")

    def test_single_redis(self, celery_setup: CeleryTestSetup):
        assert celery_setup.broker.container.id == celery_setup.backend.container.id
