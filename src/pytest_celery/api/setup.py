from celery import Celery

from pytest_celery import defaults
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

    def __len__(self) -> int:
        return len(self._worker_cluster) + len(self._broker_cluster) + len(self._backend_cluster)

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

    @classmethod
    def name(cls) -> str:
        return defaults.DEFAULT_WORKER_APP_NAME

    @classmethod
    def config(cls, celery_worker_cluster_config: dict) -> dict:
        # TODO: Check input
        celery_broker_cluster_config: dict = celery_worker_cluster_config["celery_broker_cluster_config"]
        celery_backend_cluster_config: dict = celery_worker_cluster_config["celery_backend_cluster_config"]
        return {
            "broker_url": ";".join(celery_broker_cluster_config["local_urls"]),
            "result_backend": ";".join(celery_backend_cluster_config["local_urls"]),
        }

    @classmethod
    def create_worker_app(cls, celery_worker_config: dict, celery_setup_app_name: str) -> Celery:
        # TODO: Check input
        celery_broker_config = celery_worker_config["celery_broker_config"]
        celery_backend_config = celery_worker_config["celery_backend_config"]
        app = Celery(celery_setup_app_name)
        app.config_from_object(
            {
                "broker_url": celery_broker_config["local_url"],
                "result_backend": celery_backend_config["local_url"],
            }
        )
        return app

    @classmethod
    def create_setup_app(cls, celery_setup_config: dict, celery_setup_app_name: str) -> Celery:
        # TODO: Check input
        app = Celery(celery_setup_app_name)
        app.config_from_object(celery_setup_config)
        return app
