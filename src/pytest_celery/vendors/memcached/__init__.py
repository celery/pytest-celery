"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Memcached Backend vendor.
"""

from .. import MissingCeleryDependency

try:
    import memcache  # noqa F401
except ImportError as e:
    raise MissingCeleryDependency("celery extra dependency missing: celery[pymemcache]") from e
