"""
This module contains all the default values and settings.
These values are used by the pytest-celery plugin to configure the
components fixtures. You can override these values by hooking to the
matchin fixture and returning your own value.
"""

from pytest_docker_tools import network

##########
# Docker
##########

DEFAULT_NETWORK = network()
DEFAULT_READY_TIMEOUT = 60
DEFAULT_READY_MAX_RETRIES = 3

##########
# Fixtures
##########

# These are the names of the fixtures that are used by the plugin.
# They define preconfigured components fixtures for docker containers

# Fixtures names
################

# Generic components fixtures
CELERY_SETUP = "celery_setup"
CELERY_WORKER = "celery_worker"
CELERY_WORKER_CLUSTER = "celery_worker_cluster"
CELERY_BACKEND = "celery_backend"
CELERY_BACKEND_CLUSTER = "celery_backend_cluster"
CELERY_BROKER = "celery_broker"
CELERY_BROKER_CLUSTER = "celery_broker_cluster"

# Components fixtures
CELERY_TEST_WORKER = "celery_test_worker"
CELERY_REDIS_BACKEND = "celery_redis_backend"
CELERY_REDIS_BROKER = "celery_redis_broker"
CELERY_RABBITMQ_BROKER = "celery_rabbitmq_broker"
FUNCTION_WORKER = "function_worker"
REDIS_FUNCTION_BACKEND = "redis_function_backend"
RABBITMQ_FUNCTION_BROKER = "rabbitmq_function_broker"
REDIS_FUNCTION_BROKER = "redis_function_broker"

# Fixtures collections
######################

FUNCTION_WORKERS = (FUNCTION_WORKER,)
FUNCTION_BACKENDS = (REDIS_FUNCTION_BACKEND,)
FUNCTION_BROKERS = (
    RABBITMQ_FUNCTION_BROKER,
    REDIS_FUNCTION_BROKER,
)

ALL_REDIS_FIXTURES = (
    REDIS_FUNCTION_BACKEND,
    REDIS_FUNCTION_BROKER,
)
ALL_RABBITMQ_FIXTURES = (RABBITMQ_FUNCTION_BROKER,)
ALL_WORKERS_FIXTURES = (*FUNCTION_WORKERS,)
ALL_BACKENDS_FIXTURES = (*FUNCTION_BACKENDS,)
ALL_BROKERS_FIXTURES = (*FUNCTION_BROKERS,)
ALL_COMPONENTS_FIXTURES = (
    *ALL_WORKERS_FIXTURES,
    *ALL_BACKENDS_FIXTURES,
    *ALL_BROKERS_FIXTURES,
)
ALL_NODES_FIXTURES = (
    CELERY_WORKER,
    CELERY_BACKEND,
    CELERY_BROKER,
)
ALL_CLUSTERS_FIXTURES = (
    CELERY_WORKER_CLUSTER,
    CELERY_BACKEND_CLUSTER,
    CELERY_BROKER_CLUSTER,
)
ALL_CELERY_WORKERS = (CELERY_TEST_WORKER,)
ALL_CELERY_BACKENDS = (CELERY_REDIS_BACKEND,)
ALL_CELERY_BROKERS = (
    CELERY_REDIS_BROKER,
    CELERY_RABBITMQ_BROKER,
)

##########################
# Worker Container Settings
##########################

# Default container settings for all worker container fixtures
WORKER_CELERY_APP_NAME = "celery_test_app"
WORKER_CELERY_VERSION = "5.3.0b2"
WORKER_ENV = {
    "CELERY_BROKER_URL": "memory://",
    "CELERY_RESULT_BACKEND": "cache+memory://",
    "LOG_LEVEL": "INFO",
    "PYTHONUNBUFFERED": "1",
}

# Docker containers settings
#################################################

# Function Worker #
###################
FUNCTION_WORKER_APP_NAME = WORKER_CELERY_APP_NAME
FUNCTION_WORKER_VERSION = WORKER_CELERY_VERSION
FUNCTION_WORKER_ENV = WORKER_ENV
FUNCTION_WORKER_CONTAINER_TIMEOUT = 30

##########################
# Redis Container Settings
##########################

# Default container settings for all redis container fixtures

REDIS_IMAGE = "redis:latest"
REDIS_PORTS = {"6379/tcp": None}
REDIS_ENV: dict = {}
REDIS_CONTAINER_TIMEOUT = DEFAULT_READY_TIMEOUT

# Docker containers settings
#################################################

# Function Backend #
####################
REDIS_FUNCTION_BACKEND_ENV = REDIS_ENV
REDIS_FUNCTION_BACKEND_IMAGE = REDIS_IMAGE
REDIS_FUNCTION_BACKEND_PORTS = REDIS_PORTS


# Function Broker #
###################
REDIS_FUNCTION_BROKER_ENV = REDIS_ENV
REDIS_FUNCTION_BROKER_IMAGE = REDIS_IMAGE
REDIS_FUNCTION_BROKER_PORTS = REDIS_PORTS


#############################
# RabbitMQ Container Settings
#############################

# Default container settings for all rabbitmq container fixtures

RABBITMQ_IMAGE = "rabbitmq:latest"
RABBITMQ_PORTS = {"5672/tcp": None}
RABBITMQ_ENV: dict = {}
RABBITMQ_CONTAINER_TIMEOUT = DEFAULT_READY_TIMEOUT

# Docker containers settings
#################################################

# Function Broker #
###################
RABBITMQ_FUNCTION_BROKER_ENV = RABBITMQ_ENV
RABBITMQ_FUNCTION_BROKER_IMAGE = RABBITMQ_IMAGE
RABBITMQ_FUNCTION_BROKER_PORTS = RABBITMQ_PORTS
