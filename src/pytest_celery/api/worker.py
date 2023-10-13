from typing import Set
from typing import Tuple
from typing import Type
from typing import Union

from celery import Celery
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.defaults import RESULT_TIMEOUT
from pytest_celery.vendors.worker.container import CeleryWorkerContainer


class CeleryTestWorker(CeleryTestNode):
    def __init__(self, container: CeleryTestContainer, app: Celery):
        super().__init__(container)
        self._app = app
        self.container: CeleryWorkerContainer

    @property
    def app(self) -> Celery:
        return self._app

    @property
    def version(self) -> str:
        if hasattr(self.container, "version"):
            return self.container.version()
        else:
            return "unknown"

    @property
    def log_level(self) -> str:
        return self.container.log_level()

    @property
    def worker_name(self) -> str:
        return self.container.worker_name()

    @property
    def worker_queue(self) -> str:
        return self.container.worker_queue()

    def wait_for_log(self, log: str, message: str = "", timeout: int = RESULT_TIMEOUT) -> None:
        message = message or f"Waiting for worker container '{self.name()}' to log -> {log}"
        wait_for_callable(message=message, func=lambda: log in self.logs(), timeout=timeout)


class CeleryWorkerCluster(CeleryTestCluster):
    def __init__(self, *workers: Tuple[Union[CeleryTestWorker, CeleryTestContainer]]) -> None:
        super().__init__(*workers)

    def _set_nodes(
        self,
        *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]],
        node_cls: Type[CeleryTestNode] = CeleryTestWorker,
    ) -> Tuple[CeleryTestNode]:
        return super()._set_nodes(*nodes, node_cls=node_cls)

    @property
    def versions(self) -> Set[str]:
        return {worker.version for worker in self}  # type: ignore
