from pytest_celery import defaults
from pytest_celery.api.components.cluster.node import CeleryTestNode


class CeleryTestBackend(CeleryTestNode):
    @classmethod
    def default_config(cls) -> dict:
        return {
            "url": defaults.WORKER_ENV["CELERY_RESULT_BACKEND"],
            "local_url": defaults.WORKER_ENV["CELERY_RESULT_BACKEND"],
        }
