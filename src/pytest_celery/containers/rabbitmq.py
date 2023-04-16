from time import sleep

from kombu import Connection
from pytest_docker_tools.wrappers.container import wait_for_callable

from pytest_celery import defaults
from pytest_celery.api.container import CeleryTestContainer
from pytest_celery.utils import cached_property


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

    @cached_property
    def client(self) -> Connection:
        tries = 1
        max_tries = defaults.DEFAULT_MAX_RETRIES
        while tries <= max_tries:
            try:
                celeryconfig = self.celeryconfig
                client = Connection(
                    f"amqp://localhost/{celeryconfig['vhost']}",
                    port=celeryconfig["port"],
                )
                return client
            except Exception as e:
                if tries == max_tries:
                    raise e
                tries += 1

    @cached_property
    def celeryconfig(self) -> dict:
        return {
            "url": self.url,
            "local_url": self.local_url,
            "hostname": self.hostname,
            "port": self.port,
            "vhost": self.vhost,
        }

    @cached_property
    def url(self) -> str:
        return f"amqp://{self.hostname}/{self.vhost}"

    @cached_property
    def local_url(self) -> str:
        return f"amqp://localhost:{self.port}/{self.vhost}"

    @cached_property
    def port(self) -> int:
        try:
            wait_for_callable(
                "Waiting for port to be ready",
                lambda: self.get_addr("5672/tcp"),
            )
        except IndexError:
            sleep(1)

        _, port = self.get_addr("5672/tcp")
        return port

    @cached_property
    def hostname(self) -> str:
        return self.attrs["Config"]["Hostname"]

    @cached_property
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
