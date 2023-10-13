from abc import abstractmethod
from typing import Any
from typing import Iterator
from typing import Tuple
from typing import Type
from typing import Union

from pytest_celery.api.container import CeleryTestContainer


class CeleryTestNode:
    def __init__(self, container: CeleryTestContainer):
        self._container = container

    @property
    def container(self) -> CeleryTestContainer:
        return self._container

    def ready(self) -> bool:
        return self.container.ready()

    def config(self, *args: tuple, **kwargs: dict) -> dict:
        return self.container.celeryconfig

    @classmethod
    def default_config(cls) -> dict:
        return {}

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, CeleryTestNode):
            return self.container == __value.container
        return False

    def logs(self) -> str:
        return self.container.logs()

    def name(self) -> str:
        return self.container.name

    def hostname(self) -> str:
        return self.container.id[:12]

    def kill(self) -> None:
        self.container.kill()

    def teardown(self) -> None:
        self.container.teardown()


class CeleryTestCluster:
    def __init__(self, *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> None:
        if not nodes:
            raise ValueError("At least one node is required")
        if len(nodes) == 1 and isinstance(nodes[0], list):
            nodes = tuple(node for node in nodes[0])
        if not all(isinstance(node, (CeleryTestNode, CeleryTestContainer)) for node in nodes):
            raise TypeError("All nodes must be CeleryTestNode or CeleryTestContainer")

        self.nodes = nodes  # type: ignore

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

    @property
    def nodes(self) -> Tuple[CeleryTestNode]:
        return self.s

    @nodes.setter
    def nodes(self, nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]]) -> None:
        self.s = self._set_nodes(*nodes)  # type: ignore

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
        return all(node.ready() for node in self)

    def config(self, *args: tuple, **kwargs: dict) -> dict:
        config = [node.container.celeryconfig for node in self]
        return {
            "urls": [c["url"] for c in config],
            "local_urls": [c["local_url"] for c in config],
        }

    @classmethod
    def default_config(cls) -> dict:
        return {}

    def teardown(self) -> None:
        pass
