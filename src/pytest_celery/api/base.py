"""The node/cluster set are designed to provide a common interface for
encapsulating the implementation of test components and their integration with
the test framework.

This module provides the base API for creating new components by
defining the base classes for nodes and clusters.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Iterator

import pytest_docker_tools
from celery import Celery
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.defaults import CONTAINER_TIMEOUT
from pytest_celery.defaults import RESULT_TIMEOUT


class CeleryTestNode:
    """This is the logical representation of a container instance. It is used
    to provide a common interface for interacting with the container regardless
    of the underlying implementation.

    Responsibility Scope:
        The node's responsibility is to wrap the container and provide
        useful methods for interacting with it.
    """

    def __init__(self, container: CeleryTestContainer, app: Celery = None) -> None:
        """Setup the base components of a CeleryTestNode.

        Args:
            container (CeleryTestContainer): Container to use for the node.
            app (Celery, optional): Celery app. Defaults to None.
        """
        self._container = container
        self._app = app

    @property
    def container(self) -> CeleryTestContainer:
        """Underlying container for the node."""
        return self._container

    @property
    def app(self) -> Celery:
        """Celery app for the node if available."""
        return self._app

    def __eq__(self, other: object) -> bool:
        """Two nodes are equal if they have the same container and Celery
        app."""
        if isinstance(other, CeleryTestNode):
            return all(
                (
                    self.container == other.container,
                    self.app == other.app,
                )
            )
        return False

    @classmethod
    def default_config(cls) -> dict:
        """Default node configurations if not overridden by the user."""
        return {}

    def ready(self) -> bool:
        """Waits until the node is ready or raise an exception if it fails to
        boot up."""
        return self.container.ready()

    def config(self, *args: tuple, **kwargs: dict) -> dict:
        """Compile the configurations required for Celery from this node."""
        config = self.container.celeryconfig

        if not args and not kwargs:
            return config

        for key, value in kwargs.items():
            config[key] = value

            if key == "vhost":
                vhost = str(value)
                config["url"] = f"{config['url'][:-1].rstrip('/')}/{vhost}"
                config["host_url"] = f"{config['host_url'][:-1].rstrip('/')}/{vhost}"
                config[key] = vhost

        return config

    def logs(self) -> str:
        """Get the logs of the underlying container."""
        return self.container.logs()

    def name(self) -> str:
        """Get the name of this node."""
        return self.container.name

    def hostname(self) -> str:
        """Get the hostname of this node."""
        return self.container.id[:12]

    def kill(self, signal: str | int = "SIGKILL", reload_container: bool = True) -> None:
        """Kill the underlying container.

        Args:
            signal (str | int, optional): Signal to send to the container. Defaults to "SIGKILL".
            reload_container (bool, optional): Reload the container object after killing it. Defaults to True.
        """
        if self.container.status == "running":
            self.container.kill(signal=signal)
        if reload_container:
            self.container.reload()

    def restart(self, reload_container: bool = True, force: bool = False) -> None:
        """Restart the underlying container.

        Args:
            reload_container (bool, optional): Reload the container object after restarting it. Defaults to True.
            force (bool, optional): Kill the container before restarting it. Defaults to False.
        """
        if force:
            # Use SIGTERM to allow the container to gracefully shutdown
            self.kill(signal="SIGTERM", reload_container=reload_container)
        self.container.restart(timeout=CONTAINER_TIMEOUT)
        if reload_container:
            self.container.reload()
        if self.app:
            self.app.set_current()

    def teardown(self) -> None:
        """Teardown the node."""
        self.container.teardown()

    def wait_for_log(self, log: str, message: str = "", timeout: int = RESULT_TIMEOUT) -> None:
        """Wait for a log to appear in the container.

        Args:
            log (str): Log to wait for.
            message (str, optional): Message to display while waiting. Defaults to "".
            timeout (int, optional): Timeout in seconds. Defaults to RESULT_TIMEOUT.
        """
        message = message or f"Waiting for worker container '{self.name()}' to log -> {log}"
        wait_for_callable(message=message, func=lambda: log in self.logs(), timeout=timeout)

    def assert_log_exists(self, log: str, message: str = "", timeout: int = RESULT_TIMEOUT) -> None:
        """Assert that a log exists in the container.

        Args:
            log (str): Log to assert.
            message (str, optional): Message to display while waiting. Defaults to "".
            timeout (int, optional): Timeout in seconds. Defaults to RESULT_TIMEOUT.
        """
        try:
            self.wait_for_log(log, message, timeout)
        except pytest_docker_tools.exceptions.TimeoutError:
            assert False, f"Worker container '{self.name()}' did not log -> {log} within {timeout} seconds"

    def assert_log_does_not_exist(self, log: str, message: str = "", timeout: int = 1) -> None:
        """Assert that a log does not exist in the container.

        Args:
            log (str): Log to assert.
            message (str, optional): Message to display while waiting. Defaults to "".
            timeout (int, optional): Timeout in seconds. Defaults to 1.
        """
        message = message or f"Waiting for worker container '{self.name()}' to not log -> {log}"
        try:
            self.wait_for_log(log, message, timeout)
        except pytest_docker_tools.exceptions.TimeoutError:
            return
        assert False, f"Worker container '{self.name()}' logged -> {log} within {timeout} seconds"


class CeleryTestCluster:
    """This is a collection of CeleryTestNodes. It is used to collect the test
    nodes into a single object for easier management.

    Responsibility Scope:
        The cluster's responsibility is to define which nodes will be used for
        the test.
    """

    def __init__(self, *nodes: tuple[CeleryTestNode | CeleryTestContainer]) -> None:
        """Setup the base components of a CeleryTestCluster.

        Args:
            *nodes (tuple[CeleryTestNode | CeleryTestContainer]): Nodes to use for the cluster.

        Raises:
            ValueError: At least one node is required.
            TypeError: All nodes must be CeleryTestNode or CeleryTestContainer
        """
        if not nodes:
            raise ValueError("At least one node is required")
        if len(nodes) == 1 and isinstance(nodes[0], list):
            nodes = tuple(node for node in nodes[0])
        if not all(isinstance(node, (CeleryTestNode, CeleryTestContainer)) for node in nodes):
            raise TypeError("All nodes must be CeleryTestNode or CeleryTestContainer")

        self.nodes = nodes  # type: ignore

    @property
    def nodes(self) -> tuple[CeleryTestNode]:
        """Get the nodes of the cluster."""
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: tuple[CeleryTestNode | CeleryTestContainer]) -> None:
        """Set the nodes of the cluster.

        Args:
            nodes (tuple[CeleryTestNode | CeleryTestContainer]): Nodes to use for the cluster.
        """
        self._nodes = self._set_nodes(*nodes)  # type: ignore

    def __iter__(self) -> Iterator[CeleryTestNode]:
        """Iterate over the nodes of the cluster."""
        return iter(self.nodes)

    def __getitem__(self, index: int) -> CeleryTestNode:
        """Get a node from the cluster by index."""
        return self.nodes[index]

    def __len__(self) -> int:
        """Get the number of nodes in the cluster."""
        return len(self.nodes)

    def __eq__(self, other: object) -> bool:
        """Two clusters are equal if they have the same nodes."""
        if isinstance(other, CeleryTestCluster):
            if len(self) == len(other):
                for node in self:
                    if node not in other:
                        return False
        return False

    @classmethod
    def default_config(cls) -> dict:
        """Default cluster configurations if not overridden by the user."""
        return {}

    @abstractmethod
    def _set_nodes(
        self,
        *nodes: tuple[CeleryTestNode | CeleryTestContainer],
        node_cls: type[CeleryTestNode] = CeleryTestNode,
    ) -> tuple[CeleryTestNode]:
        """Set the nodes of the cluster.

        Args:
            *nodes (tuple[CeleryTestNode | CeleryTestContainer]): Nodes to use for the cluster.
            node_cls (type[CeleryTestNode], optional): Node class to use. Defaults to CeleryTestNode.

        Returns:
            tuple[CeleryTestNode]: Nodes to use for the cluster.
        """
        return tuple(
            (
                node_cls(node)
                if isinstance(
                    node,
                    CeleryTestContainer,
                )
                else node
            )
            for node in nodes
        )  # type: ignore

    def ready(self) -> bool:
        """Waits until the cluster is ready or raise an exception if any of the
        nodes fail to boot up."""
        return all(node.ready() for node in self)

    def config(self, *args: tuple, **kwargs: dict) -> dict:
        """Compile the configurations required for Celery from this cluster."""
        config = [node.config() for node in self]
        return {
            "urls": [c["url"] for c in config],
            "host_urls": [c["host_url"] for c in config],
        }

    def teardown(self) -> None:
        """Teardown the cluster."""
        # Nodes teardown themselves, so we just need to clear the cluster
        # if there is any cleanup to do
