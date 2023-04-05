from celery.signals import after_task_publish

from pytest_celery import CeleryTestSetup
from tests.common.tasks import identity


class test_signals:
    def test_signals(self, celery_setup: CeleryTestSetup):
        signal_was_called = False

        @after_task_publish.connect
        def task_sent_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        assert signal_was_called is False
        assert identity.s("test_signals").delay().get() == "test_signals"
        assert signal_was_called is True
