from abc import abstractmethod
from typing import Tuple
from typing import Union

from pytest_celery.api.components.cluster.node import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer


class CeleryTestCluster:
    def __init__(self, *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> None:
        self.nodes = nodes

    @property
    def nodes(self) -> Tuple[CeleryTestNode]:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> None:
        self._nodes = self._set_nodes(*nodes)

    @abstractmethod
    def _set_nodes(self, *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> Tuple[CeleryTestNode]:
        pass

    def ready(self) -> bool:
        return all(node.ready() for node in self._nodes)
