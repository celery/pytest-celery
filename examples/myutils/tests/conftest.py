from types import ModuleType

import pytest

from pytest_celery import CeleryTestWorker


class MyWorker(CeleryTestWorker):

    def myfunc(self) -> bool:
        exit_code, output = self.container.exec_run(
            'python -c "from utils import myfunc; print(myfunc())"',
        )
        if exit_code != 0:
            raise RuntimeError(f"Error: {output}")
        output = output.decode("utf-8")
        return output.strip()


@pytest.fixture
def default_worker_cls() -> type[CeleryTestWorker]:
    return MyWorker


@pytest.fixture
def default_worker_utils_module() -> ModuleType:
    from tests import myutils

    return myutils
