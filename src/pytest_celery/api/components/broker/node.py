from pytest_celery import defaults
from pytest_celery.api.components.cluster.node import CeleryTestNode


class CeleryTestBroker(CeleryTestNode):
    @classmethod
    def default_config(cls) -> dict:
        return {
            "url": defaults.WORKER_ENV["CELERY_BROKER_URL"],
            "local_url": defaults.WORKER_ENV["CELERY_BROKER_URL"],
        }
