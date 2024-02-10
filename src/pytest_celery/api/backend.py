"""Backend components represents Celery's result backend instances.

This module provides the base API for creating new backend components by
defining the base classes for backend nodes and clusters.
"""

from __future__ import annotations

from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.defaults import DEFAULT_WORKER_ENV


class CeleryTestBackend(CeleryTestNode):
    """This is specialized node type for handling celery backends nodes. It is
    used to encapsulate a backend instance.

    Responsibility Scope:
        Handling backend specific requirements and configuration.
    """

    @classmethod
    def default_config(cls) -> dict:
        """Default node configurations if not overridden by the user."""
        return {
            "url": DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"],
            "host_url": DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"],
        }

    def restart(self, reload_container: bool = True, force: bool = False) -> None:
        """Override restart method to update the app result backend with new
        container values."""
        super().restart(reload_container, force)
        if self.app:
            self.app.conf.update(
                result_backend=self.config()["host_url"],
            )


class CeleryBackendCluster(CeleryTestCluster):
    """This is a specialized cluster type for handling celery backends. It is
    used to define which backend instances are available for the test.

    Responsibility Scope:
        Provude useful methods for managing a cluster of celery backends.
    """

    @classmethod
    def default_config(cls) -> dict:
        """Default cluster configurations if not overridden by the user."""
        return {
            "urls": [DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]],
            "host_urls": [DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]],
        }
