from typing import Tuple
from typing import Union

from pytest_celery.api.components.backend.node import CeleryTestBackend
from pytest_celery.api.components.cluster.base import CeleryTestCluster
from pytest_celery.api.components.cluster.node import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer


class CeleryBackendCluster(CeleryTestCluster):
    def __init__(self, *backends: Tuple[Union[CeleryTestBackend, CeleryTestContainer]]) -> None:
        super().__init__(*backends)

    def _set_nodes(self, *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> Tuple[CeleryTestNode]:
        return super()._set_nodes(*nodes, node_cls=CeleryTestBackend)
