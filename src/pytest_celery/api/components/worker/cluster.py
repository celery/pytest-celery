from typing import Set
from typing import Tuple
from typing import Type
from typing import Union

from pytest_celery.api.components.cluster.base import CeleryTestCluster
from pytest_celery.api.components.cluster.node import CeleryTestNode
from pytest_celery.api.components.worker.node import CeleryTestWorker
from pytest_celery.api.container import CeleryTestContainer


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
