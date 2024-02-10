"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Redis Backend vendor.
"""

from __future__ import annotations

import gc

from pytest_celery.api.backend import CeleryTestBackend


class RedisTestBackend(CeleryTestBackend):
    def teardown(self) -> None:
        # When a test that has a AsyncResult object is finished
        # there's a race condition between the AsyncResult object
        # and the Redis container. The AsyncResult object tries
        # to release the connection but the Redis container has already
        # exited. This causes a warning to be logged. To avoid this
        # warning to our best effort we force a garbage collection here.
        gc.collect(1)
        super().teardown()
