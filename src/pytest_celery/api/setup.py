from celery import Celery

from pytest_celery.api.components.backend.cluster import CeleryBackendCluster
from pytest_celery.api.components.broker.cluster import CeleryBrokerCluster
from pytest_celery.api.components.worker.cluster import CeleryWorkerCluster


class CeleryTestSetup:
    def __init__(
        self,
        worker_cluster: CeleryWorkerCluster,
        broker_cluster: CeleryBrokerCluster,
        backend_cluster: CeleryBackendCluster,
        app: Celery = None,
    ):
        self._worker_cluster = worker_cluster
        self._broker_cluster = broker_cluster
        self._backend_cluster = backend_cluster
        self._app = app

        from pytest_celery.components.worker.common import ping

        self.ping = ping

    @property
    def app(self) -> Celery:
        return self._app

    @property
    def worker_cluster(self) -> CeleryWorkerCluster:
        return self._worker_cluster

    @property
    def broker_cluster(self) -> CeleryBrokerCluster:
        return self._broker_cluster

    @property
    def backend_cluster(self) -> CeleryBackendCluster:
        return self._backend_cluster

    def ready(self, ping: bool = False) -> bool:
        ready = all(
            [
                self._worker_cluster.ready(),
                self._broker_cluster.ready(),
                self._backend_cluster.ready(),
            ]
        )

        r = self.app.control.ping()
        ready = all(
            [
                ready,
                all([all([res["ok"] == "pong" for _, res in response.items()]) for response in r]),
            ]
        )

        if not ping:
            return ready

        res = self.ping.s().delay()
        return ready and res.get(timeout=30) == "pong"
