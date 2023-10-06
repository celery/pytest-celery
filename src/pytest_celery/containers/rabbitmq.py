from typing import Optional

from kombu import Connection

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer


class RabbitMQContainer(CeleryTestContainer):
    @property
    def client(self) -> Connection:
        client = Connection(
            self.celeryconfig["local_url"],
            port=self.celeryconfig["port"],
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
        return self._wait_port("5672/tcp")

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

    @property
    def ready_prompt(self) -> Optional[str]:
        return "Server startup complete"
