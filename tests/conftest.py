import pytest

from tests import tasks


@pytest.fixture
def default_worker_tasks():
    default_worker_tasks = set()
    default_worker_tasks.add(tasks)
    return default_worker_tasks
