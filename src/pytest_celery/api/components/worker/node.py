from celery import Celery

from pytest_celery.api.components.cluster.node import CeleryTestNode
from pytest_celery.api.container import CeleryTestContainer


class CeleryTestWorker(CeleryTestNode):
    def __init__(self, container: CeleryTestContainer, app: Celery):
        super().__init__(container)
        self._app = app

    @property
    def app(self) -> Celery:
        return self._app

    @property
    def version(self) -> str:
        if hasattr(self.container, "version"):
            return self.container.version()
        else:
            return "unknown"
