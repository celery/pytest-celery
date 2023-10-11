from typing import Tuple
from typing import Type
from typing import Union

from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.defaults import WORKER_ENV


class CeleryTestBackend(CeleryTestNode):
    @classmethod
    def default_config(cls) -> dict:
        return {
            "url": WORKER_ENV["CELERY_RESULT_BACKEND"],
            "local_url": WORKER_ENV["CELERY_RESULT_BACKEND"],
        }


class CeleryBackendCluster(CeleryTestCluster):
    def __init__(self, *backends: Tuple[Union[CeleryTestBackend, CeleryTestContainer]]) -> None:
        super().__init__(*backends)

    def _set_nodes(
        self,
        *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]],
        node_cls: Type[CeleryTestNode] = CeleryTestBackend,
    ) -> Tuple[CeleryTestNode]:
        return super()._set_nodes(*nodes, node_cls=node_cls)

    @classmethod
    def default_config(cls) -> dict:
        return {
            "urls": [WORKER_ENV["CELERY_RESULT_BACKEND"]],
            "local_urls": [WORKER_ENV["CELERY_RESULT_BACKEND"]],
        }
