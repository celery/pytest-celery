"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Memcached Backend vendor.
"""

from __future__ import annotations

from pytest_celery.api.backend import CeleryTestBackend


class MemcachedTestBackend(CeleryTestBackend):
    pass
