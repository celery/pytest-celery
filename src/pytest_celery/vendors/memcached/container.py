from celery import platforms

if platforms.IS_WINDOWS:
    import memcache
else:
    import pylibmc as memcache

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.memcached.defaults import MEMCACHED_ENV
from pytest_celery.vendors.memcached.defaults import MEMCACHED_IMAGE
from pytest_celery.vendors.memcached.defaults import MEMCACHED_PORTS
from pytest_celery.vendors.memcached.defaults import MEMCACHED_PREFIX


class MemcachedContainer(CeleryTestContainer):
    @property
    def client(self) -> memcache.Client:
        conf = self.celeryconfig
        servers = [f"{conf['local_url'][:-1].split('://')[-1]}"]
        client = memcache.Client(servers)
        return client

    @property
    def celeryconfig(self) -> dict:
        return {
            "url": self.url,
            "local_url": self.local_url,
            "hostname": self.hostname,
            "port": self.port,
        }

    @property
    def url(self) -> str:
        return f"{MEMCACHED_PREFIX}{self.hostname}/"

    @property
    def local_url(self) -> str:
        return f"{MEMCACHED_PREFIX}localhost:{self.port}/"

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
    def env(cls) -> dict:
        return MEMCACHED_ENV

    @classmethod
    def image(cls) -> str:
        return MEMCACHED_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return MEMCACHED_PORTS
