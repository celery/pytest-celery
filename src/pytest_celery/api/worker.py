"""Worker components represents Celery's worker instances.

This module provides the base API for creating new worker components by
defining the base classes for worker nodes and clusters.
"""

from __future__ import annotations

import json

from celery import Celery

from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.worker.container import CeleryWorkerContainer


class CeleryTestWorker(CeleryTestNode):
    """This is specialized node type for handling celery worker nodes. It is
    used to encapsulate a worker instance.

    Responsibility Scope:
        Managing a celery worker.
    """

    def __init__(self, container: CeleryTestContainer, app: Celery):
        """A celery worker node must be initialized with a celery app.

        Args:
            container (CeleryTestContainer): Container to use for the node.
            app (Celery, optional): Celery app to be accessed from the tests.
        """
        super().__init__(container, app)

        # Helps with autocomplete in the IDE
        self.container: CeleryWorkerContainer

    @property
    def version(self) -> str:
        """Celery version of this worker node."""
        return self.container.version()

    @property
    def log_level(self) -> str:
        """Celery log level of this worker node."""
        return self.container.log_level()

    @property
    def worker_name(self) -> str:
        """Celery test worker node name."""
        return self.container.worker_name()

    @property
    def worker_queue(self) -> str:
        """Celery queue for this worker node."""
        return self.container.worker_queue()

    def hostname(self) -> str:
        """Hostname of the worker node."""
        return f"{self.worker_name}@{super().hostname()}"

    def get_running_processes_info(
        self,
        columns: list[str] | None = None,
        filters: dict[str, str] | None = None,
    ) -> list[dict]:
        """Get running processes info on the container of this node.

        Possible columns:
            - pid
            - name
            - username
            - cmdline
            - cpu_percent
            - memory_percent
            - create_time

        Args:
            columns (list[str] | None, optional): Columns to query. Defaults to None (all).
            filters (dict[str, str] | None, optional): Filters to apply. Defaults to None.

        Raises:
            RuntimeError: If the command fails.

        Returns:
            list[dict]: List of processes info per requested columns.
        """
        # Use special vendors/worker/content/utils.py module
        exit_code, output = self.container.exec_run(
            f'python -c "from utils import get_running_processes_info; print(get_running_processes_info({columns!r}))"'
        )

        if exit_code != 0:
            raise RuntimeError(f"Failed to get processes info: {output}")

        decoded_str = output.decode("utf-8")
        output = json.loads(decoded_str)

        if filters:
            output = [item for item in output if all(item.get(key) == value for key, value in filters.items())]

        return output


class CeleryWorkerCluster(CeleryTestCluster):
    """This is a specialized cluster type for handling celery workers. It is
    used to define which worker instances are available for the test.

    Responsibility Scope:
        Provude useful methods for managing a cluster of celery workers.
    """

    @property
    def versions(self) -> set[str]:
        """Celery versions of all workers in this cluster."""
        return {worker.version for worker in self}  # type: ignore
