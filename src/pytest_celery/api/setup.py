from __future__ import annotations

from celery import Celery

from pytest_celery.api.backend import CeleryBackendCluster
from pytest_celery.api.backend import CeleryTestBackend
from pytest_celery.api.broker import CeleryBrokerCluster
from pytest_celery.api.broker import CeleryTestBroker
from pytest_celery.api.worker import CeleryTestWorker
from pytest_celery.api.worker import CeleryWorkerCluster
from pytest_celery.defaults import DEFAULT_WORKER_APP_NAME
from pytest_celery.defaults import RESULT_TIMEOUT
from pytest_celery.vendors.worker.tasks import ping


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

        self.ping = ping

    def __len__(self) -> int:
        return len(self._worker_cluster) + len(self._broker_cluster) + len(self._backend_cluster)

    @property
    def app(self) -> Celery:
        return self._app

    @property
    def backend_cluster(self) -> CeleryBackendCluster:
        return self._backend_cluster

    @property
    def backend(self) -> CeleryTestBackend:
        return self._backend_cluster[0]  # type: ignore

    @property
    def broker_cluster(self) -> CeleryBrokerCluster:
        return self._broker_cluster

    @property
    def broker(self) -> CeleryTestBroker:
        return self._broker_cluster[0]  # type: ignore

    @property
    def worker_cluster(self) -> CeleryWorkerCluster:
        return self._worker_cluster

    @property
    def worker(self) -> CeleryTestWorker:
        return self._worker_cluster[0]  # type: ignore

    @classmethod
    def name(cls) -> str:
        return DEFAULT_WORKER_APP_NAME

    @classmethod
    def config(cls, celery_worker_cluster_config: dict) -> dict:
        if not celery_worker_cluster_config:
            raise ValueError("celery_worker_cluster_config is empty")

        celery_broker_cluster_config: dict = celery_worker_cluster_config.get("celery_broker_cluster_config", {})
        celery_backend_cluster_config: dict = celery_worker_cluster_config.get("celery_backend_cluster_config", {})
        config = {}
        if celery_broker_cluster_config:
            config["broker_url"] = ";".join(celery_broker_cluster_config["local_urls"])
        if celery_backend_cluster_config:
            config["result_backend"] = ";".join(celery_backend_cluster_config["local_urls"])
        return config

    @classmethod
    def update_app_config(cls, app: Celery) -> None:
        # Use app.conf.update() to update the app config
        pass

    @classmethod
    def create_setup_app(cls, celery_setup_config: dict, celery_setup_app_name: str) -> Celery:
        if celery_setup_config is None:
            raise ValueError("celery_setup_config is None")

        if not celery_setup_app_name:
            raise ValueError("celery_setup_app_name is empty")

        app = Celery(celery_setup_app_name)
        app.config_from_object(celery_setup_config)
        cls.update_app_config(app)

        return app

    def chords_allowed(self) -> bool:
        try:
            self.app.backend.ensure_chords_allowed()
        except NotImplementedError:
            return False

        if any([v.startswith("4.") for v in self.worker_cluster.versions]):
            return False

        return True

    def teardown(self) -> None:
        pass

    def ready(self, ping: bool = False, control: bool = False, docker: bool = True) -> bool:
        ready = True

        if docker and ready:
            if self.broker_cluster:
                ready = ready and self.broker_cluster.ready()
            if self.backend_cluster:
                ready = ready and self.backend_cluster.ready()
            if self.worker_cluster:
                ready = ready and self.worker_cluster.ready()

        if control and ready:
            r = self.app.control.ping()
            ready = ready and all([all([res["ok"] == "pong" for _, res in response.items()]) for response in r])

        if ping and ready:
            # TODO: ignore mypy globally for type overriding
            worker: CeleryTestWorker
            for worker in self.worker_cluster:  # type: ignore
                res = self.ping.s().apply_async(queue=worker.worker_queue)
                ready = ready and res.get(timeout=RESULT_TIMEOUT) == "pong"

        # Set app for all nodes
        nodes: tuple = tuple()
        if self.broker_cluster:
            nodes += self.broker_cluster.nodes
        if self.backend_cluster:
            nodes += self.backend_cluster.nodes
        if self.worker_cluster:
            nodes += self.worker_cluster.nodes
        for node in nodes:
            node._app = self.app

        return ready
