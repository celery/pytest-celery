from demoapp.tasks import add
from demoapp.tasks import count_widgets


def test_add(celery_setup):
    assert add.s(1, 2).delay().get() == 3


def test_count_widgets(celery_setup):
    assert count_widgets.s().delay().get() == 0
