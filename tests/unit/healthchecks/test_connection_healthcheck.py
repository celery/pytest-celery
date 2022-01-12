import pytest
from mocket import Mocket, mocketize

from pytest_celery.healthchecks import HealthCheckFailedError
from pytest_celery.healthchecks.connection import ConnectionHealthy


@mocketize
def test_connection_healthy(faker):
    healthcheck = ConnectionHealthy(faker.ipv4(), faker.port_number())

    healthcheck()

    assert Mocket._address == (healthcheck.endpoint, healthcheck.port)


def test_connection_unhealthy(faker):
    """
    Connection healthcheck fails because we are not using mocketize
    """
    # TODO: Raise connection error from mocketize
    healthcheck = ConnectionHealthy(faker.ipv4(), faker.port_number())

    with pytest.raises(HealthCheckFailedError):
        healthcheck()
