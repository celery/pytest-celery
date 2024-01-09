from __future__ import annotations

from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.defaults import DEFAULT_WORKER_ENV


class CeleryTestBroker(CeleryTestNode):
    """CeleryTestBroker is specialized node type for handling celery brokers
    nodes. It is used to encapsulate a broker instance.

    Responsibility Scope:
        Handling broker specific requirements and configuration.
    """

    @classmethod
    def default_config(cls) -> dict:
        return {
            "url": DEFAULT_WORKER_ENV["CELERY_BROKER_URL"],
            "local_url": DEFAULT_WORKER_ENV["CELERY_BROKER_URL"],
        }

    def restart(self, reload_container: bool = True, force: bool = False) -> None:
        super().restart(reload_container, force)
        if self.app:
            self.app.conf.update(
                broker_url=self.config()["local_url"],
            )


class CeleryBrokerCluster(CeleryTestCluster):
    """CeleryBrokerCluster is a specialized cluster type for handling celery
    brokers. It is used to define which broker instances are available for the
    test.

    Responsibility Scope:
        Provude useful methods for managing a cluster of celery brokers.
    """

    def __init__(self, *brokers: tuple[CeleryTestBroker | CeleryTestContainer]) -> None:
        super().__init__(*brokers)

    def _set_nodes(
        self,
        *nodes: tuple[CeleryTestNode | CeleryTestContainer],
        node_cls: type[CeleryTestNode] = CeleryTestBroker,
    ) -> tuple[CeleryTestNode]:
        return super()._set_nodes(*nodes, node_cls=node_cls)

    @classmethod
    def default_config(cls) -> dict:
        return {
            "urls": [DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]],
            "local_urls": [DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]],
        }
