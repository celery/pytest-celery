from pytest_celery import CeleryTestSetup
from tests.conftest import MyWorker
from tests.myutils import myfunc


def test_myfunc():
    assert myfunc() == "foo"


def test_myfunc_in_worker(celery_worker: MyWorker):
    assert celery_worker.myfunc() == "foo"
    assert celery_worker.get_running_processes_info()


def test_myfunc_in_setup_worker(celery_setup: CeleryTestSetup):
    celery_worker: MyWorker = celery_setup.worker
    assert celery_worker.myfunc() == "foo"
    assert celery_worker.get_running_processes_info()
