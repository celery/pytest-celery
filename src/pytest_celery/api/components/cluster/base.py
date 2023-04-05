# from __future__ import annotations

from abc import abstractmethod
from typing import Tuple
from typing import Type
from typing import Union

from pytest_celery.api.components.cluster.node import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer


class CeleryTestCluster:
    def __init__(self, *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> None:
        if not nodes:
            raise ValueError("At least one node is required")
        if len(nodes) == 1 and isinstance(nodes[0], list):
            nodes = tuple(node for node in nodes[0])
        if not all(isinstance(node, (CeleryTestNode, CeleryTestContainer)) for node in nodes):
            raise TypeError("All nodes must be CeleryTestNode or CeleryTestContainer")

        self.nodes = nodes  # type: ignore

    @property
    def nodes(self) -> Tuple[CeleryTestNode]:
        return self._nodes

    @nodes.setter
    def nodes(self, nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> None:
        self._nodes = self._set_nodes(*nodes)  # type: ignore

    @abstractmethod
    def _set_nodes(
        self,
        *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]],
        node_cls: Type[CeleryTestNode] = CeleryTestNode,
    ) -> Tuple[CeleryTestNode]:
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
        return all(node.ready() for node in self.nodes)
