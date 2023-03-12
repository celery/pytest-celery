from pytest_celery.api.setup import CeleryTestSetup


class test_custom_setup:
    def test_celery_setup_override(self, celery_setup: CeleryTestSetup, my_custom_setup: CeleryTestSetup):
        assert celery_setup == my_custom_setup
        assert celery_setup.ready()
