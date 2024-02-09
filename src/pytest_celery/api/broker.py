"""Broker components represents Celery's broker instances.

This module provides the base API for creating new broker components by
defining the base classes for broker nodes and clusters.
"""

from __future__ import annotations

from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.defaults import DEFAULT_WORKER_ENV


class CeleryTestBroker(CeleryTestNode):
    """This is specialized node type for handling celery brokers nodes. It is
    used to encapsulate a broker instance.

    Responsibility Scope:
        Handling broker specific requirements and configuration.
    """

    @classmethod
    def default_config(cls) -> dict:
        """Default node configurations if not overridden by the user."""
        return {
            "url": DEFAULT_WORKER_ENV["CELERY_BROKER_URL"],
            "host_url": DEFAULT_WORKER_ENV["CELERY_BROKER_URL"],
        }

    def restart(self, reload_container: bool = True, force: bool = False) -> None:
        """Override restart method to update the app broker url with new
        container values."""
        super().restart(reload_container, force)
        if self.app:
            self.app.conf.update(
                broker_url=self.config()["host_url"],
            )


class CeleryBrokerCluster(CeleryTestCluster):
    """This is a specialized cluster type for handling celery brokers. It is
    used to define which broker instances are available for the test.

    Responsibility Scope:
        Provude useful methods for managing a cluster of celery brokers.
    """

    @classmethod
    def default_config(cls) -> dict:
        """Default cluster configurations if not overridden by the user."""
        return {
            "urls": [DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]],
            "host_urls": [DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]],
        }
