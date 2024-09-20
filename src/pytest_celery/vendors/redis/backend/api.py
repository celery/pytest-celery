"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Redis Backend vendor.
"""

from __future__ import annotations

import gc

from celery.result import AsyncResult

from pytest_celery.api.backend import CeleryTestBackend


class RedisTestBackend(CeleryTestBackend):
    def teardown(self) -> None:
        """When a test that has a AsyncResult object is finished there's a race
        condition between the AsyncResult object and the Redis container.

        The AsyncResult object tries to release the connection but the
        Redis container has already exited.
        """
        # First, force a garbage collection to clean up unreachable objects
        gc.collect()

        # Next, find all live AsyncResult objects and clean them up
        async_results = [obj for obj in gc.get_objects() if isinstance(obj, AsyncResult)]

        for async_result in async_results:
            try:
                # Remove the backend reference to prevent interaction with Redis
                async_result.backend = None
            except Exception:
                pass

        super().teardown()
