"""The ``pytest_docker_tools`` package powers the Docker container management
for the plugin.

This module extends the ``Container`` class from the package to provide
the base API for creating new test containers in a Celery test environment.
"""

from __future__ import annotations

from typing import Any

import pytest_docker_tools
from pytest_docker_tools import wrappers
from pytest_docker_tools.wrappers.container import wait_for_callable
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_fixed


class CeleryTestContainer(wrappers.Container):
    """This is an extension of pytest_docker_tools.wrappers.Container, adding
    improved control over the container lifecycle.

    Responsibility Scope:
        Provide useful methods for managing a container instance.
    """

    @property
    def client(self) -> Any:
        """Provides an API client for interacting with the container, if
        available.

        Subclasses should implement this to return an instance of the client
        specific to the service running in the container.

        Raises:
            NotImplementedError: There is not client available by default.

        Returns:
            Any: Client instance.
        """
        raise NotImplementedError("CeleryTestContainer.client")

    @property
    def celeryconfig(self) -> dict:
        """Each container is responsible for providing the configuration values
        required for Celery. This property should be implemented to return the
        configuration values for the specific container.

        Raises:
            NotImplementedError: There is no config available by default.

        Returns:
            dict: Configuration values required for Celery.
        """
        raise NotImplementedError("CeleryTestContainer.celeryconfig")

    @classmethod
    def command(
        cls,
        *args: str,
        debugpy: bool = False,
        wait_for_client: bool = True,
        **kwargs: dict,
    ) -> list[str]:
        """Override the CMD instruction in the Dockerfile.

        This method should be overridden in derived classes to provide the
        specific command and its arguments required to start the container.

        Args:
            *args (str): Additional command-line arguments.
            debugpy (bool): Enable debugpy. Defaults to False.
            wait_for_client (bool): Wait for a debugger to be attached. Defaults to True.
            **kwargs (dict): Additional keyword arguments.

        Raises:
            NotImplementedError: Rely on the Dockerfile if not set otherwise by default.

        Returns:
            list[str]: A list containing the command to run in the container as
                the first element, followed by the command-line arguments.
        """

        raise NotImplementedError("CeleryTestContainer.command")

    def teardown(self) -> None:
        """Teardown the container instance."""

    @property
    def ready_prompt(self) -> str | None:
        """A log string that indicates the container has finished starting up
        and is ready to use.

        Returns:
            str | None: A string to wait for or None for no wait. Defaults to None.
        """
        return None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        retry=retry_if_exception_type(IndexError),
        reraise=True,
    )
    def _wait_port(self, port: str) -> int:
        """Blocks until the specified port is ready.

        Args:
            port (str): Port to wait for.

        Raises:
            ValueError: Port cannot be empty.

        Returns:
            int: Port number.
        """
        if not port:
            raise ValueError("Port cannot be empty")

        while not super().ready():
            pass
        _, p = self.get_addr(port)
        return p

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(10),
        retry=retry_if_exception_type(pytest_docker_tools.exceptions.TimeoutError),
        reraise=True,
    )
    def _wait_ready(self, timeout: int = 30) -> bool:
        """Wait for the container to be ready by polling the logs for the
        readiness prompt. If no prompt is set, the container is considered
        ready as soon as its live logs are accessible.

        Args:
            timeout (int, optional): Timeout in seconds. Defaults to 30.

        Returns:
            bool: True if ready, False otherwise.
        """
        if self.ready_prompt is not None:
            if self.ready_prompt not in self.logs():
                wait_for_callable(
                    f"Waiting for {self.__class__.__name__}::{self.name} to get ready",
                    lambda: self.ready_prompt in self.logs(),
                    timeout=timeout,
                )

        wait_for_callable(
            f"{self.__class__.__name__}::{self.name} is ready",
            lambda: self.ready_prompt or "" in self.logs(),
        )
        return True

    def ready(self) -> bool:
        """Override the default ready() method to wait for the container to be
        using our waiting logic on top of the default implementation.

        When this method returns False, other attempts will be made until the container
        is ready or stop if other conditions do not allow for it to be ready.
        The underlying implementation of pytest_docker_tools is currently responsible for error raising.

        Returns:
            bool: True if ready, False otherwise.
        """
        if super().ready():
            return self._wait_ready()
        else:
            return False
