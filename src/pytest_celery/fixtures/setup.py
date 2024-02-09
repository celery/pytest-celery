"""The test setup integrates all of the independent test components into a
single entry point for the test.

This module provides the fixtures for the test setup, which will be used
to prepare the environment for testing.

The test setup is automatically configured according to the individual
components of the given architecture.

A test will be parametrized for each combination of supported celery
backends, brokers, and workers in the test setup.
"""

# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest
from celery import Celery

from pytest_celery.api.backend import CeleryBackendCluster
from pytest_celery.api.broker import CeleryBrokerCluster
from pytest_celery.api.setup import CeleryTestSetup
from pytest_celery.api.worker import CeleryWorkerCluster


@pytest.fixture
def celery_setup_cls() -> type[CeleryTestSetup]:  # type: ignore
    """The setup class to use for the test."""
    return CeleryTestSetup


@pytest.fixture
def celery_setup(  # type: ignore
    celery_setup_cls: type[CeleryTestSetup],
    celery_worker_cluster: CeleryWorkerCluster,
    celery_broker_cluster: CeleryBrokerCluster,
    celery_backend_cluster: CeleryBackendCluster,
    celery_setup_app: Celery,
) -> CeleryTestSetup:
    """Prepares a celery setup ready for testing.

    This fixture provides the entry point for a test.
    This fixture loads all components and immediately prepares the environment for testing.

    Example:
        >>> def test_my_celery_setup(celery_setup: CeleryTestSetup):
        ...     assert celery_setup.ready()
        ...     # do some testing
    """
    setup = celery_setup_cls(
        worker_cluster=celery_worker_cluster,
        broker_cluster=celery_broker_cluster,
        backend_cluster=celery_backend_cluster,
        app=celery_setup_app,
    )

    # Shallow ready check for performance reasons
    assert setup.ready(
        ping=False,
        control=False,
        docker=False,
    )
    yield setup
    setup.teardown()


@pytest.fixture
def celery_setup_name(celery_setup_cls: type[CeleryTestSetup]) -> str:  # type: ignore
    """Fixture interface to the API."""
    return celery_setup_cls.name()


@pytest.fixture
def celery_setup_config(
    celery_setup_cls: type[CeleryTestSetup],
    celery_worker_cluster_config: dict,
) -> dict:
    """Fixture interface to the API."""
    return celery_setup_cls.config(
        celery_worker_cluster_config=celery_worker_cluster_config,
    )


@pytest.fixture
def celery_setup_app(
    celery_setup_cls: type[CeleryTestSetup],
    celery_setup_config: dict,
    celery_setup_name: str,
) -> Celery:
    """Fixture interface to the API."""
    return celery_setup_cls.create_setup_app(
        celery_setup_config=celery_setup_config,
        celery_setup_app_name=celery_setup_name,
    )
