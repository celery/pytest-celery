from itertools import count

from pytest_celery.api.container import CeleryTestContainer


class CeleryTestNode:
    def __init__(self, container: CeleryTestContainer):
        self._container = container

    @property
    def container(self) -> CeleryTestContainer:
        return self._container

    def ready(self) -> bool:
        for tries in count(1):
            if tries > 3:
                break
            if self.container.ready():
                return True
        else:
            raise RuntimeError(f"Can't get node to be ready: {self.container.name}")
