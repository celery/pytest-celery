"""Pytest-celery entry point."""

# Backward compatibility with pytest-celery < 1.0.0
from celery.contrib.pytest import *  # noqa

# pytest-celery >= 1.0.0 infrastructure
from pytest_celery import *  # noqa
