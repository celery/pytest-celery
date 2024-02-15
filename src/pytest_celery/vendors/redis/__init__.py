"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Redis vendor.
"""

from .. import MissingCeleryDependency

try:
    import redis  # noqa F401
except ImportError as e:
    raise MissingCeleryDependency("celery extra dependency missing: celery[redis]") from e
