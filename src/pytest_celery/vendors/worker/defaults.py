"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the :ref:`built-in-worker` vendor.
"""

from pkg_resources import resource_filename

CELERY_SETUP_WORKER = "celery_setup_worker"
DEFAULT_WORKER = "default_worker_container"
WORKER_DOCKERFILE_ROOTDIR = resource_filename("pytest_celery.vendors.worker", "")
WORKER_CELERY_APP_NAME = "celery_test_app"
WORKER_CELERY_VERSION = ""  # latest from pypi
WORKER_LOG_LEVEL = "INFO"
WORKER_NAME = "celery_test_worker"
WORKER_QUEUE = "celery"
WORKER_ENV = {
    "CELERY_BROKER_URL": "memory://",
    "CELERY_RESULT_BACKEND": "cache+memory://",
    "PYTHONUNBUFFERED": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTHONPATH": "/app",
}
WORKER_DEBUGPY_PORTS = {
    "5678/tcp": "5678",
}
WORKER_VOLUME = {
    "bind": "/app",
    "mode": "rw",
}
DEFAULT_WORKER_APP_NAME = WORKER_CELERY_APP_NAME
DEFAULT_WORKER_VERSION = WORKER_CELERY_VERSION
DEFAULT_WORKER_LOG_LEVEL = WORKER_LOG_LEVEL
DEFAULT_WORKER_NAME = WORKER_NAME
DEFAULT_WORKER_ENV = WORKER_ENV
DEFAULT_WORKER_PORTS = None
DEFAULT_WORKER_QUEUE = WORKER_QUEUE
DEFAULT_WORKER_CONTAINER_TIMEOUT = 60
DEFAULT_WORKER_VOLUME = WORKER_VOLUME
