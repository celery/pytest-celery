from demoapp.tasks import add
from demoapp.tasks import count_widgets

from pytest_celery import CeleryTestSetup


def test_add(celery_setup: CeleryTestSetup):
    assert add.s(1, 2).delay().get() == 3


def test_count_widgets(celery_setup: CeleryTestSetup):
    assert count_widgets.s().delay().get() == 0
