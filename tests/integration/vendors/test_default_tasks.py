import pytest

from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryTestSetup
from pytest_celery import add
from pytest_celery import add_replaced
from pytest_celery import fail
from pytest_celery import identity
from pytest_celery import noop
from pytest_celery import ping
from pytest_celery import sleep
from pytest_celery import xsum


class test_default_tasks:
    def test_add(self, celery_setup: CeleryTestSetup):
        assert add.s(1, 2).apply_async(queue=celery_setup.worker.worker_queue).get(timeout=RESULT_TIMEOUT) == 3

    def test_add_replaced(self, celery_setup: CeleryTestSetup):
        queue = celery_setup.worker.worker_queue
        add_replaced.s(1, 2, queue=queue).apply_async(queue=queue)
        celery_setup.worker.assert_log_exists("ignored")

    def test_fail(self, celery_setup: CeleryTestSetup):
        with pytest.raises(RuntimeError):
            fail.s().apply_async(queue=celery_setup.worker.worker_queue).get(timeout=RESULT_TIMEOUT)

    def test_identity(self, celery_setup: CeleryTestSetup):
        assert identity.s(1).apply_async(queue=celery_setup.worker.worker_queue).get(timeout=RESULT_TIMEOUT) == 1

    def test_noop(self, celery_setup: CeleryTestSetup):
        assert noop.s().apply_async(queue=celery_setup.worker.worker_queue).get(timeout=RESULT_TIMEOUT) is None

    def test_ping(self, celery_setup: CeleryTestSetup):
        assert ping.s().apply_async(queue=celery_setup.worker.worker_queue).get(timeout=RESULT_TIMEOUT) == "pong"

    def test_sleep(self, celery_setup: CeleryTestSetup):
        assert sleep.s().apply_async(queue=celery_setup.worker.worker_queue).get(timeout=RESULT_TIMEOUT) is True

    def test_xsum(self, celery_setup: CeleryTestSetup):
        assert xsum.s([1, 2, 3]).apply_async(queue=celery_setup.worker.worker_queue).get(timeout=RESULT_TIMEOUT) == 6

    def test_xsum_nested_list(self, celery_setup: CeleryTestSetup):
        assert (
            xsum.s([[1, 2], [3, 4], [5, 6]])
            .apply_async(queue=celery_setup.worker.worker_queue)
            .get(timeout=RESULT_TIMEOUT)
            == 21
        )
