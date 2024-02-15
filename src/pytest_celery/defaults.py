# flake8: noqa

from __future__ import annotations

from pytest_docker_tools import network

from pytest_celery.vendors import MissingCeleryDependency
from pytest_celery.vendors.rabbitmq.defaults import CELERY_RABBITMQ_BROKER
from pytest_celery.vendors.rabbitmq.defaults import *
from pytest_celery.vendors.worker.defaults import CELERY_SETUP_WORKER
from pytest_celery.vendors.worker.defaults import *

try:
    import pytest_celery.vendors.memcached
except MissingCeleryDependency:
    _CELERY_MEMCACHED_BACKEND = None
else:
    from pytest_celery.vendors.memcached.defaults import CELERY_MEMCACHED_BACKEND as _CELERY_MEMCACHED_BACKEND
    from pytest_celery.vendors.memcached.defaults import *

    _CELERY_MEMCACHED_BACKEND = None  # Beta support at the moment, to be used manually

try:
    import pytest_celery.vendors.redis
except MissingCeleryDependency:
    _CELERY_REDIS_BACKEND = None
    _CELERY_REDIS_BROKER = None
else:
    from pytest_celery.vendors.redis.backend.defaults import CELERY_REDIS_BACKEND as _CELERY_REDIS_BACKEND
    from pytest_celery.vendors.redis.backend.defaults import *
    from pytest_celery.vendors.redis.broker.defaults import CELERY_REDIS_BROKER as _CELERY_REDIS_BROKER
    from pytest_celery.vendors.redis.broker.defaults import *
    from pytest_celery.vendors.redis.defaults import *


####################################################################################
# Automatic components
####################################################################################

# The following collections are used to parametrize the user's tests
# according to the components they need to run against. By default,
# all possible combinations are used.

# When a new component is added to the corresponding collection it
# will automatically add it to the parametrization of every (relevant) test IMPLICITLY!
# Tests that do not rely on default parametrization will not be affected.

ALL_CELERY_WORKERS = (CELERY_SETUP_WORKER,)
ALL_CELERY_BACKENDS = (backend for backend in [_CELERY_REDIS_BACKEND, _CELERY_MEMCACHED_BACKEND] if backend is not None)
ALL_CELERY_BROKERS = (broker for broker in [CELERY_RABBITMQ_BROKER, _CELERY_REDIS_BROKER] if broker is not None)

####################################################################################
# Fixtures
####################################################################################

# These fixtures are used by pytest-celery plugin to setup the environment for the user's tests.
# They function as the main interface into the test environment's components.
# They are directly affected by the automatic collections: ALL_CELERY_WORKERS, ALL_CELERY_BACKENDS, ALL_CELERY_BROKERS.

CELERY_SETUP = "celery_setup"
CELERY_WORKER = "celery_worker"
CELERY_WORKER_CLUSTER = "celery_worker_cluster"
CELERY_BACKEND = "celery_backend"
CELERY_BACKEND_CLUSTER = "celery_backend_cluster"
CELERY_BROKER = "celery_broker"
CELERY_BROKER_CLUSTER = "celery_broker_cluster"

####################################################################################
# Docker
####################################################################################

# Default timeouts for Docker-related operations in seconds.

# Defines how long to wait for a Docker container to get ready.
CONTAINER_TIMEOUT = 60

# Specifies the maximum duration to wait for a task result.
# It's primarily used when testing Celery tasks to ensure they complete within a reasonable timeframe.
# and is set for a recommended value for most use cases.
RESULT_TIMEOUT = 60

default_pytest_celery_network = network()
