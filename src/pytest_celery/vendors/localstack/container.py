"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Localstack Broker vendor.
"""

from __future__ import annotations

from kombu import Connection

from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.vendors.localstack.defaults import LOCALSTACK_ENV
from pytest_celery.vendors.localstack.defaults import LOCALSTACK_IMAGE
from pytest_celery.vendors.localstack.defaults import LOCALSTACK_PORTS
from pytest_celery.vendors.localstack.defaults import LOCALSTACK_PREFIX


class LocalstackContainer(CeleryTestContainer):
    """This class manages the lifecycle of a Localstack container."""

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
        }

    @property
    def url(self) -> str:
        return f"{self.prefix()}{self.hostname}:4566"

    @property
    def host_url(self) -> str:
        return f"{self.prefix()}localhost:{self.port}"

    @property
    def hostname(self) -> str:
        return self.attrs["Config"]["Hostname"]

    @property
    def port(self) -> int:
        return self._wait_port("4566/tcp")

    @classmethod
    def version(cls) -> str:
        return cls.image().split("/")[-1]

    @classmethod
    def initial_env(cls) -> dict:
        return LOCALSTACK_ENV

    @classmethod
    def image(cls) -> str:
        return LOCALSTACK_IMAGE

    @classmethod
    def ports(cls) -> dict:
        return LOCALSTACK_PORTS

    @classmethod
    def prefix(cls) -> str:
        return LOCALSTACK_PREFIX

    @property
    def ready_prompt(self) -> str | None:
        return "Ready."
