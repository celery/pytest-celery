"""Default plugin configurations.

This module contains the default configurations for the pytest-celery
plugin. It also contains the automatic collections that are used to
parametrize the user's tests according to the components they need to
run against. By default, all possible combinations are used.
"""

# flake8: noqa

from __future__ import annotations

from pytest_docker_tools import network

from pytest_celery.vendors import _is_vendor_installed
from pytest_celery.vendors.localstack.defaults import CELERY_LOCALSTACK_BROKER
from pytest_celery.vendors.localstack.defaults import *
from pytest_celery.vendors.memcached.defaults import CELERY_MEMCACHED_BACKEND
from pytest_celery.vendors.memcached.defaults import *
from pytest_celery.vendors.rabbitmq.defaults import CELERY_RABBITMQ_BROKER
from pytest_celery.vendors.rabbitmq.defaults import *
from pytest_celery.vendors.redis.backend.defaults import CELERY_REDIS_BACKEND
from pytest_celery.vendors.redis.backend.defaults import *
from pytest_celery.vendors.redis.broker.defaults import CELERY_REDIS_BROKER
from pytest_celery.vendors.redis.broker.defaults import *
from pytest_celery.vendors.redis.defaults import *
from pytest_celery.vendors.worker.defaults import CELERY_SETUP_WORKER
from pytest_celery.vendors.worker.defaults import *

####################################################################################
# Automatic components
####################################################################################

# The following collections are used to parametrize the user's tests
# according to the components they need to run against. By default,
# all possible combinations are used.

# When a new component is added to the corresponding collection it
# will automatically add it to the parametrization of every (relevant) test IMPLICITLY!
# Tests that do not rely on default parametrization will not be affected.


ALL_CELERY_BACKENDS = set()
ALL_CELERY_BROKERS = set()

if _is_vendor_installed("redis"):
    ALL_CELERY_BACKENDS.add(CELERY_REDIS_BACKEND)
    ALL_CELERY_BROKERS.add(CELERY_REDIS_BROKER)

if _is_vendor_installed("rabbitmq"):
    # Uses Kombu
    ALL_CELERY_BROKERS.add(CELERY_RABBITMQ_BROKER)

# Memcached is disabled by default regardless of its availability due to its experimental status.
if _is_vendor_installed("memcached") and False:
    ALL_CELERY_BACKENDS.add(CELERY_MEMCACHED_BACKEND)

# Localstack is disabled by default regardless of its availability due to its beta status.
if _is_vendor_installed("localstack") and False:
    # Uses Kombu
    ALL_CELERY_BROKERS.add(CELERY_LOCALSTACK_BROKER)

# Worker setup is assumed to be always available.
ALL_CELERY_WORKERS = (CELERY_SETUP_WORKER,)

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
