"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Redis Broker vendor.
"""

from __future__ import annotations

from pytest_celery.api.broker import CeleryTestBroker


class RedisTestBroker(CeleryTestBroker):
    pass
