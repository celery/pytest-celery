"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Redis vendor.
"""

REDIS_IMAGE = "redis:latest"
REDIS_PORTS = {"6379/tcp": None}
REDIS_ENV: dict = {}
REDIS_CONTAINER_TIMEOUT = 60
REDIS_PREFIX = "redis://"
