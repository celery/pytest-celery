"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Memcached Backend vendor.
"""

CELERY_MEMCACHED_BACKEND = "celery_memcached_backend"
DEFAULT_MEMCACHED_BACKEND = "default_memcached_backend"
MEMCACHED_IMAGE = "memcached:latest"
MEMCACHED_PORTS = {"11211/tcp": None}
MEMCACHED_ENV: dict = {}
MEMCACHED_CONTAINER_TIMEOUT = 60
MEMCACHED_PREFIX = "cache+memcached://"
