# flake8: noqa

from pytest_docker_tools import network

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

##########
# Fixtures
##########

CELERY_SETUP = "celery_setup"
CELERY_WORKER = "celery_worker"
CELERY_WORKER_CLUSTER = "celery_worker_cluster"
CELERY_BACKEND = "celery_backend"
CELERY_BACKEND_CLUSTER = "celery_backend_cluster"
CELERY_BROKER = "celery_broker"
CELERY_BROKER_CLUSTER = "celery_broker_cluster"

######################
# Fixtures collections
######################

# These collections define which components are used by
# pytest-celery by default. If not specified otherwise, the
# user's tests will have a matrix of all possible combinations automatically

ALL_CELERY_WORKERS = (CELERY_SETUP_WORKER,)
ALL_CELERY_BACKENDS = (
    CELERY_REDIS_BACKEND,
    CELERY_MEMCACHED_BACKEND,
)
ALL_CELERY_BROKERS = (
    CELERY_REDIS_BROKER,
    CELERY_RABBITMQ_BROKER,
)

##########
# Docker
##########

CONTAINER_TIMEOUT = 60
RESULT_TIMEOUT = 60


default_pytest_celery_network = network()
