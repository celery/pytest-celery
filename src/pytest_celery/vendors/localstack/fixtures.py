"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Localstack Broker vendor.
"""

# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest
from pytest_docker_tools import container
from pytest_docker_tools import fxtr

from pytest_celery.vendors.localstack.api import LocalstackTestBroker
from pytest_celery.vendors.localstack.container import LocalstackContainer
from pytest_celery.vendors.localstack.defaults import LOCALSTACK_CONTAINER_TIMEOUT


@pytest.fixture
def celery_localstack_broker(default_localstack_broker: LocalstackContainer) -> LocalstackTestBroker:
    """Creates a LocalstackTestBroker instance. Responsible for tearing down
    the node.

    Args:
        default_localstack_broker (LocalstackContainer): Instantiated LocalstackContainer.
    """
    broker = LocalstackTestBroker(default_localstack_broker)
    yield broker
    broker.teardown()


@pytest.fixture
def default_localstack_broker_cls() -> type[LocalstackContainer]:
    """Default Localstack broker container class. Override to apply custom
    configuration globally.

    See also: :ref:`vendor-class`.

    Returns:
        type[LocalstackContainer]: API for managing the vendor's container.
    """
    return LocalstackContainer


default_localstack_broker = container(
    image="{default_localstack_broker_image}",
    ports=fxtr("default_localstack_broker_ports"),
    environment=fxtr("default_localstack_broker_env"),
    network="{default_pytest_celery_network.name}",
    wrapper_class=LocalstackContainer,
    timeout=LOCALSTACK_CONTAINER_TIMEOUT,
)


@pytest.fixture
def default_localstack_broker_env(default_localstack_broker_cls: type[LocalstackContainer]) -> dict:
    """Environment variables for this vendor.

    Args:
        default_localstack_broker_cls (type[LocalstackContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Items to pass to the container's environment.
    """
    return default_localstack_broker_cls.initial_env()


@pytest.fixture
def default_localstack_broker_image(default_localstack_broker_cls: type[LocalstackContainer]) -> str:
    """Sets the image name for this vendor.

    Args:
        default_localstack_broker_cls (type[LocalstackContainer]): See also: :ref:`vendor-class`.

    Returns:
        str: Docker image name.
    """
    return default_localstack_broker_cls.image()


@pytest.fixture
def default_localstack_broker_ports(default_localstack_broker_cls: type[LocalstackContainer]) -> dict:
    """Port bindings for this vendor.

    Args:
        default_localstack_broker_cls (type[LocalstackContainer]): See also: :ref:`vendor-class`.

    Returns:
        dict: Port bindings.
    """
    return default_localstack_broker_cls.ports()
