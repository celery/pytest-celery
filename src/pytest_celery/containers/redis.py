from typing import Optional

from redis import StrictRedis as Redis

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class RedisContainer(CeleryTestContainer):
    __ready_prompt__ = "Ready to accept connections"

    def ready(self) -> bool:
        return self._full_ready(self.__ready_prompt__)

    def _full_ready(self, match_log: str = "", check_client: bool = True) -> bool:
        ready = super()._full_ready(match_log, check_client)
        if ready and check_client:
            c: Redis = self.client  # type: ignore
            if c.ping():
                c.set("ready", "1")
                ready = c.get("ready") == "1"
                c.delete("ready")
        return ready

    @property
    def client(self) -> Optional[Redis]:
        celeryconfig = self.celeryconfig
        client = Redis.from_url(
            celeryconfig["local_url"],
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

    @property
    def url(self) -> str:
        return f"redis://{self.hostname}/{self.vhost}"

    @property
    def local_url(self) -> str:
        return f"redis://localhost:{self.port}/{self.vhost}"

    @property
    def hostname(self) -> str:
        return self.attrs["Config"]["Hostname"]

    @property
    def port(self) -> int:
        return self._port("6379/tcp")

    @property
    def vhost(self) -> str:
        return "0"

    @classmethod
    def version(cls) -> str:
        return cls.image().split(":")[-1]

    @classmethod
    def env(cls) -> dict:
        return defaults.DEFAULT_REDIS_BACKEND_ENV

    @classmethod
    def image(cls) -> str:
        return defaults.DEFAULT_REDIS_BACKEND_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return defaults.DEFAULT_REDIS_BACKEND_PORTS
