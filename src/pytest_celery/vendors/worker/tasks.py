"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the :ref:`built-in-worker` vendor.
"""

from celery import shared_task


@shared_task
def ping() -> str:
    """Pytest-celery internal task.

    Used to check if the worker is up and running.
    """
    return "pong"
