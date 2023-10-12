from pytest_celery import CELERY_BACKEND
from pytest_celery import CELERY_BACKEND_CLUSTER
from pytest_celery import CELERY_BROKER
from pytest_celery import CELERY_BROKER_CLUSTER
from pytest_celery import CELERY_WORKER
from pytest_celery import CELERY_WORKER_CLUSTER
from pytest_celery import DEFAULT_MEMCACHED_BACKEND
from pytest_celery import DEFAULT_RABBITMQ_BROKER
from pytest_celery import DEFAULT_REDIS_BACKEND
from pytest_celery import DEFAULT_REDIS_BROKER
from pytest_celery import DEFAULT_WORKER

DEFAULT_WORKERS = (DEFAULT_WORKER,)
DEFAULT_BACKENDS = (
    DEFAULT_REDIS_BACKEND,
    DEFAULT_MEMCACHED_BACKEND,
)
DEFAULT_BROKERS = (
    DEFAULT_RABBITMQ_BROKER,
    DEFAULT_REDIS_BROKER,
)

ALL_REDIS_FIXTURES = (
    DEFAULT_REDIS_BACKEND,
    DEFAULT_REDIS_BROKER,
)
ALL_RABBITMQ_FIXTURES = (DEFAULT_RABBITMQ_BROKER,)
ALL_MEMCACHED_FIXTURES = (DEFAULT_MEMCACHED_BACKEND,)
ALL_WORKERS_FIXTURES = (*DEFAULT_WORKERS,)
ALL_BACKENDS_FIXTURES = (*DEFAULT_BACKENDS,)
ALL_BROKERS_FIXTURES = (*DEFAULT_BROKERS,)
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
