"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Memcached Backend vendor.
"""

from __future__ import annotations

import memcache

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.memcached.defaults import MEMCACHED_ENV
from pytest_celery.vendors.memcached.defaults import MEMCACHED_IMAGE
from pytest_celery.vendors.memcached.defaults import MEMCACHED_PORTS
from pytest_celery.vendors.memcached.defaults import MEMCACHED_PREFIX


class MemcachedContainer(CeleryTestContainer):
    """This class manages the lifecycle of a Memcached container."""

    @property
    def client(self) -> memcache.Client:
        conf = self.celeryconfig
        servers = [f"{conf['host_url'][:-1].split('://')[-1]}"]
        client = memcache.Client(servers)
        return client

    @property
    def celeryconfig(self) -> dict:
        return {
            "url": self.url,
            "host_url": self.host_url,
            "hostname": self.hostname,
            "port": self.port,
        }

    @property
    def url(self) -> str:
        return f"{self.prefix()}{self.hostname}/"

    @property
    def host_url(self) -> str:
        return f"{self.prefix()}localhost:{self.port}/"

    @property
    def hostname(self) -> str:
        return self.attrs["Config"]["Hostname"]

    @property
    def port(self) -> int:
        return self._wait_port("11211/tcp")

    @classmethod
    def version(cls) -> str:
        return cls.image().split(":")[-1]

    @classmethod
    def initial_env(cls) -> dict:
        return MEMCACHED_ENV

    @classmethod
    def image(cls) -> str:
        return MEMCACHED_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return MEMCACHED_PORTS

    @classmethod
    def prefix(cls) -> str:
        return MEMCACHED_PREFIX
