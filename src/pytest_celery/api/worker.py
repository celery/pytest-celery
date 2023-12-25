from __future__ import annotations

import json

from celery import Celery

from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.worker.container import CeleryWorkerContainer


class CeleryTestWorker(CeleryTestNode):
    def __init__(self, container: CeleryTestContainer, app: Celery):
        super().__init__(container, app)

        # Helps with autocomplete in the IDE
        self.container: CeleryWorkerContainer

    @property
    def version(self) -> str:
        return self.container.version()

    @property
    def log_level(self) -> str:
        return self.container.log_level()

    @property
    def worker_name(self) -> str:
        return self.container.worker_name()

    @property
    def worker_queue(self) -> str:
        return self.container.worker_queue()

    def hostname(self) -> str:
        return f"{self.worker_name}@{super().hostname()}"

    def get_running_processes_info(
        self,
        columns: list[str] | None = None,
        filters: dict[str, str] | None = None,
    ) -> list[dict]:
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
    def __init__(self, *workers: tuple[CeleryTestWorker | CeleryTestContainer]) -> None:
        super().__init__(*workers)

    def _set_nodes(
        self,
        *nodes: tuple[CeleryTestNode | CeleryTestContainer],
        node_cls: type[CeleryTestNode] = CeleryTestWorker,
    ) -> tuple[CeleryTestNode]:
        return super()._set_nodes(*nodes, node_cls=node_cls)

    @property
    def versions(self) -> set[str]:
        return {worker.version for worker in self}  # type: ignore
