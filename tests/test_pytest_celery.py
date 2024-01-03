import pytest

import pytest_celery


def test_version():
    assert pytest_celery.VERSION
    assert len(pytest_celery.VERSION) >= 3
    pytest_celery.VERSION = (0, 3, 0)
    assert pytest_celery.__version__.count(".") >= 2


@pytest.mark.parametrize(
    "attr",
    [
        "__author__",
        "__contact__",
        "__homepage__",
        "__docformat__",
    ],
)
def test_meta(attr):
    assert getattr(pytest_celery, attr, None)
