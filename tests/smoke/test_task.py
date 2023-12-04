from __future__ import annotations

from celery import signature

from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryTestSetup
from tests.tasks import add
from tests.tasks import identity
from tests.tasks import replace_with_task


class test_replace:
    def test_sanity(self, celery_setup: CeleryTestSetup):
        queues = [w.worker_queue for w in celery_setup.worker_cluster]
        if len(queues) < 2:
            queues.append(queues[0])
        replace_with = signature(identity, args=(40,), queue=queues[1])
        sig1 = replace_with_task.s(replace_with)
        sig2 = add.s(2).set(queue=queues[1])
        c = sig1 | sig2
        r = c.apply_async(queue=queues[0])
        assert r.get(timeout=RESULT_TIMEOUT) == 42
