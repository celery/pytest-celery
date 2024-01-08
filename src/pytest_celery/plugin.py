"""Pytest-celery entry point."""

# pytest-celery < 1.0.0 infrastructure
from celery.contrib.pytest import *  # noqa

# pytest-celery >= 1.0.0 infrastructure
from pytest_celery import *  # noqa
