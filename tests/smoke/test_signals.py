from __future__ import annotations

import pytest
from celery.signals import after_task_publish
from celery.signals import before_task_publish

from pytest_celery import CeleryTestSetup
from tests.tasks import noop


@pytest.fixture
def default_worker_signals(default_worker_signals: set) -> set:
    from tests.smoke import signals

    default_worker_signals.add(signals)
    yield default_worker_signals


class test_signals:
    @pytest.mark.parametrize(
        "log, control",
        [
            ("worker_init_handler", None),
            ("worker_process_init_handler", None),
            ("worker_ready_handler", None),
            ("worker_process_shutdown_handler", "shutdown"),
            ("worker_shutdown_handler", "shutdown"),
        ],
    )
    def test_sanity(self, celery_setup: CeleryTestSetup, log: str, control: str):
        if control:
            celery_setup.app.control.broadcast(control)
        celery_setup.worker.assert_log_exists(log)

    def test_before_task_publish(self, celery_setup: CeleryTestSetup):
        @before_task_publish.connect
        def before_task_publish_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        signal_was_called = False
        noop.s().apply_async(queue=celery_setup.worker.worker_queue)
        assert signal_was_called is True

    def test_after_task_publish(self, celery_setup: CeleryTestSetup):
        @after_task_publish.connect
        def after_task_publish_handler(*args, **kwargs):
            nonlocal signal_was_called
            signal_was_called = True

        signal_was_called = False
        noop.s().apply_async(queue=celery_setup.worker.worker_queue)
        assert signal_was_called is True
