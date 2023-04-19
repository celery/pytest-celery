from kombu import Connection

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class RabbitMQContainer(CeleryTestContainer):
    __ready_prompt__ = "Server startup complete"

    def ready(self) -> bool:
        return self._full_ready(self.__ready_prompt__)

    def _full_ready(self, match_log: str = "", check_client: bool = True) -> bool:
        ready = super()._full_ready(match_log, check_client)
        if ready and check_client:
            c: Connection = self.client  # type: ignore
            try:
                ready = bool(c.connect())
            finally:
                c.release()
        return ready

    @property
    def client(self) -> Connection:
        celeryconfig = self.celeryconfig
        client = Connection(
            f"amqp://localhost/{celeryconfig['vhost']}",
            port=celeryconfig["port"],
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
        return f"amqp://{self.hostname}/{self.vhost}"

    @property
    def local_url(self) -> str:
        return f"amqp://localhost:{self.port}/{self.vhost}"

    @property
    def hostname(self) -> str:
        return self.attrs["Config"]["Hostname"]

    @property
    def port(self) -> int:
        return self._port("5672/tcp")

    @property
    def vhost(self) -> str:
        return "/"

    @classmethod
    def version(cls) -> str:
        return cls.image().split(":")[-1]

    @classmethod
    def env(cls) -> dict:
        return defaults.DEFAULT_RABBITMQ_BROKER_ENV

    @classmethod
    def image(cls) -> str:
        return defaults.DEFAULT_RABBITMQ_BROKER_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return defaults.DEFAULT_RABBITMQ_BROKER_PORTS
