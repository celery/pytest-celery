import pytest


@pytest.fixture
def default_worker_tasks(default_worker_tasks: set) -> set:
    from tests import tasks

    default_worker_tasks.add(tasks)
    yield default_worker_tasks
