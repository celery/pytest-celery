from pytest_celery.api.container import CeleryTestContainer


class UnitTestContainer(CeleryTestContainer):
    def client(self):
        return self
