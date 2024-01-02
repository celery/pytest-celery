import pytest_celery


def test_version():
    assert pytest_celery.VERSION
    assert len(pytest_celery.VERSION) >= 3
    pytest_celery.VERSION = (0, 3, 0)
    assert pytest_celery.__version__.count(".") >= 2
