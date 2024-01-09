"""Pytest-celery entry point.

The new pytest-celery plugin is a complete new infrastructure for
testing Celery applications. It enables the legacy testing
infrastructure for maintaining backwards compatibility with pytest-
celery < 1.0.0.

The legacy testing infrastructure is maintained under the celery
project.
"""

# pytest-celery < 1.0.0 infrastructure
from celery.contrib.pytest import *  # noqa

# pytest-celery >= 1.0.0 infrastructure
from pytest_celery import *  # noqa
