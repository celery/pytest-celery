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
        return {
            "url": DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"],
            "local_url": DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"],
        }

    def restart(self, reload_container: bool = True, force: bool = False) -> None:
        """Override restart method to update the app result backend with new
        container values."""
        super().restart(reload_container, force)
        if self.app:
            self.app.conf.update(
                result_backend=self.config()["local_url"],
            )


class CeleryBackendCluster(CeleryTestCluster):
    """This is a specialized cluster type for handling celery backends. It is
    used to define which backend instances are available for the test.

    Responsibility Scope:
        Provude useful methods for managing a cluster of celery backends.
    """

    @classmethod
    def default_config(cls) -> dict:
        return {
            "urls": [DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]],
            "local_urls": [DEFAULT_WORKER_ENV["CELERY_RESULT_BACKEND"]],
        }
