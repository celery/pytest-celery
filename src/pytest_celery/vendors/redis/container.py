from __future__ import annotations

from redis import StrictRedis as Redis

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.redis.defaults import REDIS_ENV
from pytest_celery.vendors.redis.defaults import REDIS_IMAGE
from pytest_celery.vendors.redis.defaults import REDIS_PORTS
from pytest_celery.vendors.redis.defaults import REDIS_PREFIX


class RedisContainer(CeleryTestContainer):
    @property
    def client(self) -> Redis | None:
        client = Redis.from_url(
            self.celeryconfig["local_url"],
            decode_responses=True,
        )
        return client

    @property
    def celeryconfig(self) -> dict:
        return {
            "url": self.url,
            "local_url": self.local_url,
            "hostname": self.hostname,
            "port": self.port,
            "vhost": self.vhost,
        }

    @classmethod
    def command(cls, *args: str) -> list:
        return ["redis-server", *args]

    @property
    def url(self) -> str:
        return f"{self.prefix()}{self.hostname}/{self.vhost}"

    @property
    def local_url(self) -> str:
        return f"{self.prefix()}localhost:{self.port}/{self.vhost}"

    @property
    def hostname(self) -> str:
        return self.attrs["Config"]["Hostname"]

    @property
    def port(self) -> int:
        return self._wait_port("6379/tcp")

    @property
    def vhost(self) -> str:
        return "0"

    @classmethod
    def version(cls) -> str:
        return cls.image().split(":")[-1]

    @classmethod
    def env(cls) -> dict:
        return REDIS_ENV

    @classmethod
    def image(cls) -> str:
        return REDIS_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return REDIS_PORTS

    @classmethod
    def prefix(cls) -> str:
        return REDIS_PREFIX

    @property
    def ready_prompt(self) -> str | None:
        return "Ready to accept connections"
