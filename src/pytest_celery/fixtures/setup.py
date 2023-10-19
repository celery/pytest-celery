# mypy: disable-error-code="misc"

from typing import Type

import pytest
from celery import Celery

from pytest_celery.api.backend import CeleryBackendCluster
from pytest_celery.api.broker import CeleryBrokerCluster
from pytest_celery.api.setup import CeleryTestSetup
from pytest_celery.api.worker import CeleryWorkerCluster


@pytest.fixture
def celery_setup_cls() -> Type[CeleryTestSetup]:  # type: ignore
    return CeleryTestSetup


@pytest.fixture
def celery_setup(  # type: ignore
    celery_setup_cls: Type[CeleryTestSetup],
    celery_worker_cluster: CeleryWorkerCluster,
    celery_broker_cluster: CeleryBrokerCluster,
    celery_backend_cluster: CeleryBackendCluster,
    celery_setup_app: Celery,
) -> CeleryTestSetup:
    setup = celery_setup_cls(
        worker_cluster=celery_worker_cluster,
        broker_cluster=celery_broker_cluster,
        backend_cluster=celery_backend_cluster,
        app=celery_setup_app,
    )
    assert setup.ready(
        ping=False,
        control=False,
        docker=False,
    )
    yield setup
    setup.teardown()


@pytest.fixture
def celery_setup_name(celery_setup_cls: Type[CeleryTestSetup]) -> str:  # type: ignore
    yield celery_setup_cls.name()


@pytest.fixture
def celery_setup_config(
    celery_setup_cls: Type[CeleryTestSetup],
    celery_worker_cluster_config: dict,
) -> dict:
    yield celery_setup_cls.config(
        celery_worker_cluster_config=celery_worker_cluster_config,
    )


@pytest.fixture
def celery_setup_app(
    celery_setup_cls: Type[CeleryTestSetup],
    celery_setup_config: dict,
    celery_setup_name: str,
) -> Celery:
    yield celery_setup_cls.create_setup_app(
        celery_setup_config=celery_setup_config,
        celery_setup_app_name=celery_setup_name,
    )
