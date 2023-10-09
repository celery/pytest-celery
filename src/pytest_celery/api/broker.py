from typing import Tuple
from typing import Type
from typing import Union

from pytest_celery import defaults
from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer


class CeleryTestBroker(CeleryTestNode):
    @classmethod
    def default_config(cls) -> dict:
        return {
            "url": defaults.WORKER_ENV["CELERY_BROKER_URL"],
            "local_url": defaults.WORKER_ENV["CELERY_BROKER_URL"],
        }


class CeleryBrokerCluster(CeleryTestCluster):
    def __init__(self, *brokers: Tuple[Union[CeleryTestBroker, CeleryTestContainer]]) -> None:
        super().__init__(*brokers)

    def _set_nodes(
        self,
        *nodes: Tuple[Union[CeleryTestNode, CeleryTestContainer]],
        node_cls: Type[CeleryTestNode] = CeleryTestBroker,
    ) -> Tuple[CeleryTestNode]:
        return super()._set_nodes(*nodes, node_cls=node_cls)

    @classmethod
    def default_config(cls) -> dict:
        return {
            "urls": [defaults.WORKER_ENV["CELERY_BROKER_URL"]],
            "local_urls": [defaults.WORKER_ENV["CELERY_BROKER_URL"]],
        }
