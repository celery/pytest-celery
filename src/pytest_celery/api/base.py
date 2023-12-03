from __future__ import annotations

from abc import abstractmethod
from typing import Any
from typing import Iterator

import pytest_docker_tools
from celery import Celery
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.defaults import CONTAINER_TIMEOUT
from pytest_celery.defaults import RESULT_TIMEOUT


class CeleryTestNode:
    def __init__(self, container: CeleryTestContainer, app: Celery = None) -> None:
        self._container = container
        self._app = app

    @property
    def container(self) -> CeleryTestContainer:
        return self._container

    @property
    def app(self) -> Celery:
        return self._app

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, CeleryTestNode):
            return all(
                (
                    self.container == __value.container,
                    self.app == __value.app,
                )
            )
        return False

    @classmethod
    def default_config(cls) -> dict:
        return {}

    def ready(self) -> bool:
        return self.container.ready()

    def config(self, *args: tuple, **kwargs: dict) -> dict:
        return self.container.celeryconfig

    def logs(self) -> str:
        return self.container.logs()

    def name(self) -> str:
        return self.container.name

    def hostname(self) -> str:
        return self.container.id[:12]

    def kill(self, signal: str | int = "SIGKILL", reload_container: bool = True) -> None:
        if self.container.status == "running":
            self.container.kill(signal=signal)
        if reload_container:
            self.container.reload()

    def restart(self, reload_container: bool = True, force: bool = False) -> None:
        if force:
            self.kill(signal="SIGTERM", reload_container=reload_container)
        self.container.restart(timeout=CONTAINER_TIMEOUT)
        if reload_container:
            self.container.reload()
        if self.app:
            self.app.set_current()

    def teardown(self) -> None:
        self.container.teardown()

    def wait_for_log(self, log: str, message: str = "", timeout: int = RESULT_TIMEOUT) -> None:
        message = message or f"Waiting for worker container '{self.name()}' to log -> {log}"
        wait_for_callable(message=message, func=lambda: log in self.logs(), timeout=timeout)

    def assert_log_exists(self, log: str, message: str = "", timeout: int = RESULT_TIMEOUT) -> None:
        try:
            self.wait_for_log(log, message, timeout)
        except pytest_docker_tools.exceptions.TimeoutError:
            assert False, f"Worker container '{self.name()}' did not log -> {log} within {timeout} seconds"

    def assert_log_does_not_exist(self, log: str, message: str = "", timeout: int = 1) -> None:
        message = message or f"Waiting for worker container '{self.name()}' to not log -> {log}"
        try:
            self.wait_for_log(log, message, timeout)
        except pytest_docker_tools.exceptions.TimeoutError:
            return
        assert False, f"Worker container '{self.name()}' logged -> {log} within {timeout} seconds"


class CeleryTestCluster:
    def __init__(self, *nodes: tuple[CeleryTestNode | CeleryTestContainer]) -> None:
        if not nodes:
            raise ValueError("At least one node is required")
        if len(nodes) == 1 and isinstance(nodes[0], list):
            nodes = tuple(node for node in nodes[0])
        if not all(isinstance(node, (CeleryTestNode, CeleryTestContainer)) for node in nodes):
            raise TypeError("All nodes must be CeleryTestNode or CeleryTestContainer")

        self.nodes = nodes  # type: ignore

    @property
    def nodes(self) -> tuple[CeleryTestNode]:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: tuple[CeleryTestNode | CeleryTestContainer]) -> None:
        self._nodes = self._set_nodes(*nodes)  # type: ignore

    def __iter__(self) -> Iterator[CeleryTestNode]:
        return iter(self.nodes)

    def __getitem__(self, index: Any) -> CeleryTestNode:
        return self.nodes[index]

    def __len__(self) -> int:
        return len(self.nodes)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, CeleryTestCluster):
            for node in self:
                if node not in __value:
                    return False
        return False

    @classmethod
    def default_config(cls) -> dict:
        return {}

    @abstractmethod
    def _set_nodes(
        self,
        *nodes: tuple[CeleryTestNode | CeleryTestContainer],
        node_cls: type[CeleryTestNode] = CeleryTestNode,
    ) -> tuple[CeleryTestNode]:
        return tuple(
            node_cls(node)
            if isinstance(
                node,
                CeleryTestContainer,
            )
            else node
            for node in nodes
        )  # type: ignore

    def ready(self) -> bool:
        return all(node.ready() for node in self)

    def config(self, *args: tuple, **kwargs: dict) -> dict:
        config = [node.container.celeryconfig for node in self]
        return {
            "urls": [c["url"] for c in config],
            "local_urls": [c["local_url"] for c in config],
        }

    def teardown(self) -> None:
        # Do not need to call teardown on the nodes
        # but only tear down self
        pass
