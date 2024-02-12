"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the RabbitMQ Broker vendor.
"""

from __future__ import annotations

from kombu import Connection

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.rabbitmq.defaults import RABBITMQ_ENV
from pytest_celery.vendors.rabbitmq.defaults import RABBITMQ_IMAGE
from pytest_celery.vendors.rabbitmq.defaults import RABBITMQ_PORTS
from pytest_celery.vendors.rabbitmq.defaults import RABBITMQ_PREFIX


class RabbitMQContainer(CeleryTestContainer):
    """This class manages the lifecycle of a RabbitMQ container."""

    @property
    def client(self) -> Connection:
        client = Connection(
            self.celeryconfig["host_url"],
            port=self.celeryconfig["port"],
        )
        return client

    @property
    def celeryconfig(self) -> dict:
        return {
            "url": self.url,
            "host_url": self.host_url,
            "hostname": self.hostname,
            "port": self.port,
            "vhost": self.vhost,
        }

    @property
    def url(self) -> str:
        return f"{self.prefix()}{self.hostname}/{self.vhost}"

    @property
    def host_url(self) -> str:
        return f"{self.prefix()}localhost:{self.port}/{self.vhost}"

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
    def initial_env(cls) -> dict:
        return RABBITMQ_ENV

    @classmethod
    def image(cls) -> str:
        return RABBITMQ_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return RABBITMQ_PORTS

    @classmethod
    def prefix(cls) -> str:
        return RABBITMQ_PREFIX

    @property
    def ready_prompt(self) -> str | None:
        return "Server startup complete"
