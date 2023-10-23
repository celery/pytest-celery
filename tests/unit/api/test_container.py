from pytest_celery import CeleryTestContainer


class test_celery_test_container:
    def test_client(self, unit_tests_container: CeleryTestContainer):
        # TODO: Use mock instead of real container
        # TODO: Check raises NotImplementedError and remove the client overload from the unit tests container
        assert unit_tests_container.client == unit_tests_container
