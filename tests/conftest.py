import pytest


@pytest.fixture
def default_worker_tasks() -> set:
    from tests import tasks

    yield {tasks}
