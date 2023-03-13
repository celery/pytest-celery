from pytest_celery.api.container import CeleryTestContainer


class test_celery_test_container:
    def test_client(self, unit_tests_container: CeleryTestContainer):
        assert unit_tests_container.client()
