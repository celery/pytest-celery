"""Official pytest plugin for Celery."""

# flake8: noqa


__version__ = "1.2.1"
__author__ = "Tomer Nosrati"
__contact__ = "tomer.nosrati@gmail.com"
__homepage__ = "https://pytest-celery.readthedocs.io/"
__docformat__ = "restructuredtext"


import re
from collections import namedtuple

from pytest_celery.api.backend import CeleryBackendCluster
from pytest_celery.api.backend import CeleryTestBackend
from pytest_celery.api.base import CeleryTestCluster
from pytest_celery.api.base import CeleryTestNode
from pytest_celery.api.broker import CeleryBrokerCluster
from pytest_celery.api.broker import CeleryTestBroker
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.api.setup import CeleryTestSetup
from pytest_celery.api.worker import CeleryTestWorker
from pytest_celery.api.worker import CeleryWorkerCluster
from pytest_celery.defaults import *
from pytest_celery.fixtures.backend import celery_backend
from pytest_celery.fixtures.backend import celery_backend_cluster
from pytest_celery.fixtures.backend import celery_backend_cluster_config
from pytest_celery.fixtures.broker import celery_broker
from pytest_celery.fixtures.broker import celery_broker_cluster
from pytest_celery.fixtures.broker import celery_broker_cluster_config
from pytest_celery.fixtures.setup import celery_setup
from pytest_celery.fixtures.setup import celery_setup_app
from pytest_celery.fixtures.setup import celery_setup_cls
from pytest_celery.fixtures.setup import celery_setup_config
from pytest_celery.fixtures.setup import celery_setup_name
from pytest_celery.fixtures.worker import celery_worker
from pytest_celery.fixtures.worker import celery_worker_cluster
from pytest_celery.fixtures.worker import celery_worker_cluster_config
from pytest_celery.vendors import _is_vendor_installed

if _is_vendor_installed("localstack"):
    from pytest_celery.vendors.localstack.api import LocalstackTestBroker
    from pytest_celery.vendors.localstack.container import LocalstackContainer
    from pytest_celery.vendors.localstack.defaults import *
    from pytest_celery.vendors.localstack.fixtures import celery_localstack_broker
    from pytest_celery.vendors.localstack.fixtures import default_localstack_broker
    from pytest_celery.vendors.localstack.fixtures import default_localstack_broker_cls
    from pytest_celery.vendors.localstack.fixtures import default_localstack_broker_env
    from pytest_celery.vendors.localstack.fixtures import default_localstack_broker_image
    from pytest_celery.vendors.localstack.fixtures import default_localstack_broker_ports

if _is_vendor_installed("memcached"):
    from pytest_celery.vendors.memcached.api import MemcachedTestBackend
    from pytest_celery.vendors.memcached.container import MemcachedContainer
    from pytest_celery.vendors.memcached.defaults import *
    from pytest_celery.vendors.memcached.fixtures import celery_memcached_backend
    from pytest_celery.vendors.memcached.fixtures import default_memcached_backend
    from pytest_celery.vendors.memcached.fixtures import default_memcached_backend_cls
    from pytest_celery.vendors.memcached.fixtures import default_memcached_backend_env
    from pytest_celery.vendors.memcached.fixtures import default_memcached_backend_image
    from pytest_celery.vendors.memcached.fixtures import default_memcached_backend_ports

if _is_vendor_installed("rabbitmq"):
    from pytest_celery.vendors.rabbitmq.api import RabbitMQTestBroker
    from pytest_celery.vendors.rabbitmq.container import RabbitMQContainer
    from pytest_celery.vendors.rabbitmq.defaults import *
    from pytest_celery.vendors.rabbitmq.fixtures import celery_rabbitmq_broker
    from pytest_celery.vendors.rabbitmq.fixtures import default_rabbitmq_broker
    from pytest_celery.vendors.rabbitmq.fixtures import default_rabbitmq_broker_cls
    from pytest_celery.vendors.rabbitmq.fixtures import default_rabbitmq_broker_env
    from pytest_celery.vendors.rabbitmq.fixtures import default_rabbitmq_broker_image
    from pytest_celery.vendors.rabbitmq.fixtures import default_rabbitmq_broker_ports

if _is_vendor_installed("redis"):
    from pytest_celery.vendors.redis.backend.api import RedisTestBackend
    from pytest_celery.vendors.redis.backend.defaults import *
    from pytest_celery.vendors.redis.backend.fixtures import celery_redis_backend
    from pytest_celery.vendors.redis.backend.fixtures import default_redis_backend
    from pytest_celery.vendors.redis.backend.fixtures import default_redis_backend_cls
    from pytest_celery.vendors.redis.backend.fixtures import default_redis_backend_command
    from pytest_celery.vendors.redis.backend.fixtures import default_redis_backend_env
    from pytest_celery.vendors.redis.backend.fixtures import default_redis_backend_image
    from pytest_celery.vendors.redis.backend.fixtures import default_redis_backend_ports
    from pytest_celery.vendors.redis.broker.api import RedisTestBroker
    from pytest_celery.vendors.redis.broker.defaults import *
    from pytest_celery.vendors.redis.broker.fixtures import celery_redis_broker
    from pytest_celery.vendors.redis.broker.fixtures import default_redis_broker
    from pytest_celery.vendors.redis.broker.fixtures import default_redis_broker_cls
    from pytest_celery.vendors.redis.broker.fixtures import default_redis_broker_command
    from pytest_celery.vendors.redis.broker.fixtures import default_redis_broker_env
    from pytest_celery.vendors.redis.broker.fixtures import default_redis_broker_image
    from pytest_celery.vendors.redis.broker.fixtures import default_redis_broker_ports
    from pytest_celery.vendors.redis.container import RedisContainer
    from pytest_celery.vendors.redis.defaults import *

if _is_vendor_installed("worker"):
    from pytest_celery.vendors.worker.container import CeleryWorkerContainer
    from pytest_celery.vendors.worker.content import app
    from pytest_celery.vendors.worker.content import utils
    from pytest_celery.vendors.worker.fixtures import celery_base_worker_image
    from pytest_celery.vendors.worker.fixtures import celery_setup_worker
    from pytest_celery.vendors.worker.fixtures import default_worker_app
    from pytest_celery.vendors.worker.fixtures import default_worker_app_module
    from pytest_celery.vendors.worker.fixtures import default_worker_celery_log_level
    from pytest_celery.vendors.worker.fixtures import default_worker_celery_version
    from pytest_celery.vendors.worker.fixtures import default_worker_celery_worker_name
    from pytest_celery.vendors.worker.fixtures import default_worker_celery_worker_queue
    from pytest_celery.vendors.worker.fixtures import default_worker_cls
    from pytest_celery.vendors.worker.fixtures import default_worker_command
    from pytest_celery.vendors.worker.fixtures import default_worker_container
    from pytest_celery.vendors.worker.fixtures import default_worker_container_cls
    from pytest_celery.vendors.worker.fixtures import default_worker_container_session_cls
    from pytest_celery.vendors.worker.fixtures import default_worker_env
    from pytest_celery.vendors.worker.fixtures import default_worker_initial_content
    from pytest_celery.vendors.worker.fixtures import default_worker_ports
    from pytest_celery.vendors.worker.fixtures import default_worker_signals
    from pytest_celery.vendors.worker.fixtures import default_worker_tasks
    from pytest_celery.vendors.worker.fixtures import default_worker_utils_module
    from pytest_celery.vendors.worker.fixtures import default_worker_volume
    from pytest_celery.vendors.worker.tasks import *
    from pytest_celery.vendors.worker.volume import WorkerInitialContent


version_info_t = namedtuple(
    "version_info_t",
    (
        "major",
        "minor",
        "micro",
        "releaselevel",
        "serial",
    ),
)


# Required for RTD to build
_temp = re.match(r"v?(\d+)\.(\d+)\.(\d+)([a-zA-Z0-9]+)?", __version__).groups()  # type: ignore
VERSION = version_info = version_info_t(int(_temp[0]), int(_temp[1]), int(_temp[2]), _temp[3] or "", "")
del _temp
del re
