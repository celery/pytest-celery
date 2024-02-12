"""The test setup represents the main entry point for accessing the celery
architecture from the test.

This module provides the base API for creating new test setups.
"""

from __future__ import annotations

from celery import Celery

from pytest_celery.api.backend import CeleryBackendCluster
from pytest_celery.api.backend import CeleryTestBackend
from pytest_celery.api.broker import CeleryBrokerCluster
from pytest_celery.api.broker import CeleryTestBroker
from pytest_celery.api.worker import CeleryTestWorker
from pytest_celery.api.worker import CeleryWorkerCluster
from pytest_celery.defaults import DEFAULT_WORKER_APP_NAME
from pytest_celery.defaults import RESULT_TIMEOUT
from pytest_celery.vendors.worker.tasks import ping


class CeleryTestSetup:
    """The test setup is the main entry point for accessing the celery
    architecture from the test. It is the glue that holds all of the relevant
    components of the specific test case environment.

    Each test case will have its own test setup instance, which is created for the
    test case by the plugin and is configured for the specific run and its given configurations.

    Responsibility Scope:
        Provide useful access to the celery architecture from the test.
    """

    def __init__(
        self,
        worker_cluster: CeleryWorkerCluster,
        broker_cluster: CeleryBrokerCluster,
        backend_cluster: CeleryBackendCluster,
        app: Celery = None,
    ):
        """Setup the base components of a setup.

        Args:
            worker_cluster (CeleryWorkerCluster): Precorfigured worker cluster.
            broker_cluster (CeleryBrokerCluster): Precorfigured broker cluster.
            backend_cluster (CeleryBackendCluster): Precorfigured backend cluster.
            app (Celery, optional): Celery app configured for all of the nodes. Defaults to None.
        """
        self._worker_cluster = worker_cluster
        self._broker_cluster = broker_cluster
        self._backend_cluster = backend_cluster
        self._app = app

        # Special internal ping task, does not conflict with user "ping" tasks
        self.ping = ping

    def __len__(self) -> int:
        """The total number of nodes in the setup."""
        nodes_count = 0
        if self.broker_cluster:
            nodes_count += len(self.broker_cluster)
        if self.backend_cluster:
            nodes_count += len(self.backend_cluster)
        if self.worker_cluster:
            nodes_count += len(self.worker_cluster)
        return nodes_count

    @property
    def app(self) -> Celery:
        """The celery app configured for all of the nodes."""
        return self._app

    @property
    def backend_cluster(self) -> CeleryBackendCluster | None:
        """The backend cluster of this setup."""
        return self._backend_cluster

    @property
    def backend(self) -> CeleryTestBackend | None:
        """The first backend node of the backend cluster."""
        return self._backend_cluster[0] if self._backend_cluster else None  # type: ignore

    @property
    def broker_cluster(self) -> CeleryBrokerCluster | None:
        """The broker cluster of this setup."""
        return self._broker_cluster

    @property
    def broker(self) -> CeleryTestBroker | None:
        """The first broker node of the broker cluster."""
        return self._broker_cluster[0] if self._broker_cluster else None  # type: ignore

    @property
    def worker_cluster(self) -> CeleryWorkerCluster | None:
        """The worker cluster of this setup."""
        return self._worker_cluster

    @property
    def worker(self) -> CeleryTestWorker | None:
        """The first worker node of the worker cluster."""
        return self._worker_cluster[0] if self._worker_cluster else None  # type: ignore

    @classmethod
    def name(cls) -> str:
        """The name of the setup."""
        # TODO: Possibly not needed/required refactoring
        return DEFAULT_WORKER_APP_NAME

    @classmethod
    def config(cls, celery_worker_cluster_config: dict) -> dict:
        """Creates a configuration dict to be used by app.config_from_object().
        The configuration is compiled from all of the nodes in the setup.

        Args:
            celery_worker_cluster_config (dict): The configuration of the worker cluster.

        Returns:
            dict: Celery-aware configuration dict.
        """
        if not celery_worker_cluster_config:
            raise ValueError("celery_worker_cluster_config is empty")

        celery_broker_cluster_config: dict = celery_worker_cluster_config.get("celery_broker_cluster_config", {})
        celery_backend_cluster_config: dict = celery_worker_cluster_config.get("celery_backend_cluster_config", {})
        config = {}
        if celery_broker_cluster_config:
            config["broker_url"] = ";".join(celery_broker_cluster_config["host_urls"])
        if celery_backend_cluster_config:
            config["result_backend"] = ";".join(celery_backend_cluster_config["host_urls"])
        return config

    @classmethod
    def update_app_config(cls, app: Celery) -> None:
        """Hook for updating the app configuration in a subclass.

        Args:
            app (Celery): App after initial configuration.
        """

    @classmethod
    def create_setup_app(cls, celery_setup_config: dict, celery_setup_app_name: str) -> Celery:
        """Creates a celery app for the setup.

        Args:
            celery_setup_config (dict): Celery configuration dict.
            celery_setup_app_name (str): Celery app name.

        Returns:
            Celery: Celery app configured for this setup.
        """
        if celery_setup_config is None:
            raise ValueError("celery_setup_config is None")

        if not celery_setup_app_name:
            raise ValueError("celery_setup_app_name is empty")

        app = Celery(celery_setup_app_name)
        app.config_from_object(celery_setup_config)
        cls.update_app_config(app)

        return app

    def teardown(self) -> None:
        """Teardown the setup."""

    def ready(self, ping: bool = False, control: bool = False, docker: bool = True) -> bool:
        """Check if the setup is ready for testing. All of the confirmations
        are optional.

        Warning:
            Enabling additional confirmations may hurt performance.
            Disabling all confirmations may result in false positive results.
            Use with caution.

        Args:
            ping (bool, optional): Confirm via ping task. Defaults to False.
            control (bool, optional): Confirm via ping control. Defaults to False.
            docker (bool, optional): Confirm via docker container status. Defaults to True.

        Returns:
            bool: True if the setup is ready for testing (all required confirmations passed).
        """
        ready = (
            self._is_task_ping_ready(ping) and self._is_control_ping_ready(control) and self._is_docker_ready(docker)
        )

        if ready:
            self._set_app_for_all_nodes()

        return ready

    def _is_docker_ready(self, docker: bool) -> bool:
        """Check if the node's containers are ready.

        Args:
            docker (bool): Flag to enable docker readiness check.

        Returns:
            bool: True if the node's containers are ready, False otherwise.
        """
        if not docker:
            return True

        return (
            (not self.broker_cluster or self.broker_cluster.ready())
            and (not self.backend_cluster or self.backend_cluster.ready())
            and (not self.worker_cluster or self.worker_cluster.ready())
        )

    def _is_control_ping_ready(self, control: bool) -> bool:
        """Check if worker nodes respond to control ping.

        Args:
            control (bool): Flag to enable control ping check.

        Returns:
            bool: True if control pings are successful, False otherwise.
        """
        if not control:
            return True

        responses = self.app.control.ping()
        return all([all([res["ok"] == "pong" for _, res in response.items()]) for response in responses])

    def _is_task_ping_ready(self, ping: bool) -> bool:
        """Check if worker nodes respond to ping task.

        Args:
            ping (bool): Flag to enable ping task check.

        Returns:
            bool: True if ping tasks are successful, False otherwise.
        """
        if not ping:
            return True

        worker: CeleryTestWorker
        for worker in self.worker_cluster:  # type: ignore
            res = self.ping.s().apply_async(queue=worker.worker_queue)
            if res.get(timeout=RESULT_TIMEOUT) != "pong":
                return False
        return True

    def _set_app_for_all_nodes(self) -> None:
        """Set the app instance for all nodes in the setup.

        This ensures each node has a reference to the centralized Celery
        app instance.
        """
        nodes: tuple = tuple()
        if self.broker_cluster:
            nodes += self.broker_cluster.nodes
        if self.backend_cluster:
            nodes += self.backend_cluster.nodes
        if self.worker_cluster:
            nodes += self.worker_cluster.nodes

        for node in nodes:
            node._app = self.app
