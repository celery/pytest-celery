"""Official pytest plugin for Celery."""

# flake8: noqa


__version__ = "1.0.0b2"
__author__ = "Tomer Nosrati"
__contact__ = "tomer.nosrati@gmail.com"
__homepage__ = "https://pytest-celery.readthedocs.io/"
__docformat__ = "restructuredtext"


import re
from collections import namedtuple

from pytest_celery.api.backend import *
from pytest_celery.api.base import *
from pytest_celery.api.broker import *
from pytest_celery.api.container import *
from pytest_celery.api.setup import *
from pytest_celery.api.worker import *
from pytest_celery.defaults import *
from pytest_celery.fixtures.backend import *
from pytest_celery.fixtures.broker import *
from pytest_celery.fixtures.setup import *
from pytest_celery.fixtures.worker import *
from pytest_celery.vendors.memcached.api import *
from pytest_celery.vendors.memcached.container import *
from pytest_celery.vendors.memcached.fixtures import *
from pytest_celery.vendors.rabbitmq.api import *
from pytest_celery.vendors.rabbitmq.container import *
from pytest_celery.vendors.rabbitmq.fixtures import *
from pytest_celery.vendors.redis.backend.api import *
from pytest_celery.vendors.redis.backend.fixtures import *
from pytest_celery.vendors.redis.broker.api import *
from pytest_celery.vendors.redis.broker.fixtures import *
from pytest_celery.vendors.redis.container import *
from pytest_celery.vendors.worker.container import *
from pytest_celery.vendors.worker.content import app
from pytest_celery.vendors.worker.content import utils
from pytest_celery.vendors.worker.fixtures import *
from pytest_celery.vendors.worker.tasks import *
from pytest_celery.vendors.worker.volume import *

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
