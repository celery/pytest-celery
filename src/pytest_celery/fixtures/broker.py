"""Every broker component is added to the test matrix using the fixtures of
this module.

These fixtures will configure the test setup for all supported celery
brokers by default. Every broker will be executed as a separate test
case, and the test will be executed for each supported celery broker.

You may override these fixtures to customize the test setup for your
specific needs.
"""

# mypy: disable-error-code="misc"

from __future__ import annotations

import pytest

from pytest_celery.api.broker import CeleryBrokerCluster
from pytest_celery.api.broker import CeleryTestBroker
from pytest_celery.defaults import ALL_CELERY_BROKERS
from pytest_celery.defaults import CELERY_BROKER_CLUSTER


@pytest.fixture(params=ALL_CELERY_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:  # type: ignore
    """Parameterized fixture for all supported celery brokers. Responsible for
    tearing down the node.

    This fixture will add parametrization to the test function, so that
    the test will be executed for each supported celery broker.
    """
    broker: CeleryTestBroker = request.getfixturevalue(request.param)
    yield broker
    broker.teardown()


@pytest.fixture
def celery_broker_cluster(celery_broker: CeleryTestBroker) -> CeleryBrokerCluster:  # type: ignore
    """Defines the cluster of broker nodes for the test. Responsible for
    tearing down the cluster.

    It is not recommended to disable the broker cluster, but it can be done by
    overriding this fixture and returning None.

    Args:
        celery_broker (CeleryTestBroker): Parameterized fixture for all supported celery brokers.

    Returns:
        CeleryBrokerCluster: Single node cluster for all supported celery brokers.
    """
    cluster = CeleryBrokerCluster(celery_broker)  # type: ignore
    yield cluster
    cluster.teardown()


@pytest.fixture
def celery_broker_cluster_config(request: pytest.FixtureRequest) -> dict | None:
    """Attempts to compile the celery configuration from the cluster."""
    try:
        use_default_config = pytest.fail.Exception
        cluster: CeleryBrokerCluster = request.getfixturevalue(CELERY_BROKER_CLUSTER)
        return cluster.config() if cluster else None
    except use_default_config:
        return CeleryBrokerCluster.default_config()
