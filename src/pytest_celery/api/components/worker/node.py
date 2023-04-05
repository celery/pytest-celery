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
