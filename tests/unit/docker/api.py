from pytest_celery import CeleryTestContainer


class UnitTestContainer(CeleryTestContainer):
    def client(self):
        return self
