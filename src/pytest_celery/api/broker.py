from typing import Tuple
from typing import Type
from typing import Union

from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.defaults import WORKER_ENV


class CeleryTestBroker(CeleryTestNode):
    @classmethod
    def default_config(cls) -> dict:
        return {
            "url": WORKER_ENV["CELERY_BROKER_URL"],
            "local_url": WORKER_ENV["CELERY_BROKER_URL"],
        }

    def restart(self) -> None:
        super().restart()
        self._app.conf.update(
            broker_url=self.config()["local_url"],
        )


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
            "urls": [WORKER_ENV["CELERY_BROKER_URL"]],
            "local_urls": [WORKER_ENV["CELERY_BROKER_URL"]],
        }
