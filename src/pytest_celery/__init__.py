"""
pytest-celery a shim pytest plugin to enable celery.contrib.pytest
"""

# flake8: noqa


__version__ = "1.0.0a2"


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
from pytest_celery.vendors.worker.fixtures import *

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

# bumpversion can only search for {current_version}
# so we have to parse the version here.
_temp = re.match(r"(\d+)\.(\d+).(\d+)(.+)?", __version__).groups()  # type: ignore
VERSION = version_info = version_info_t(int(_temp[0]), int(_temp[1]), int(_temp[2]), _temp[3] or "", "")
del _temp
del re
