import pytest

from pytest_celery import defaults
from pytest_celery.api.components.backend import CeleryBackendCluster
from pytest_celery.api.components.backend import CeleryTestBackend


@pytest.fixture(params=defaults.ALL_CELERY_BACKENDS)
def celery_backend(request: pytest.FixtureRequest) -> CeleryTestBackend:
    return request.getfixturevalue(request.param)


@pytest.fixture
def celery_backend_cluster(celery_backend: CeleryTestBackend) -> CeleryBackendCluster:
    return CeleryBackendCluster(celery_backend)  # type: ignore


@pytest.fixture
def celery_backend_config(request: pytest.FixtureRequest) -> dict:
    try:
        celery_backend: CeleryTestBackend = request.getfixturevalue(defaults.CELERY_BACKEND)
        return celery_backend.container.celeryconfig()
    except BaseException:
        return {
            "url": defaults.WORKER_ENV["CELERY_RESULT_BACKEND"],
            "local_url": defaults.WORKER_ENV["CELERY_RESULT_BACKEND"],
        }
