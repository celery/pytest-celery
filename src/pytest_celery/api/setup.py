from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster


class CeleryTestSetup:
    def __init__(self, backend_cluster: CeleryBackendCluster, broker_cluster: CeleryBrokerCluster):
        self._backend_cluster = backend_cluster
        self._broker_cluster = broker_cluster

    @property
    def backend_cluster(self) -> CeleryBackendCluster:
        return self._backend_cluster

    @property
    def broker_cluster(self) -> CeleryBrokerCluster:
        return self._broker_cluster

    def ready(self) -> bool:
        return all(
            [
                self._backend_cluster.ready(),
                self._broker_cluster.ready(),
            ]
        )
