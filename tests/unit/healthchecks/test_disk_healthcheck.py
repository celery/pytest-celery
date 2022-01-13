import os
from unittest.mock import MagicMock

import pytest

from pytest_celery.healthchecks import HealthCheckFailedError
from pytest_celery.healthchecks.disk import DiskSpaceAvailable


def test_disk_space_available(faker):
    healthcheck = DiskSpaceAvailable(faker.file_path())
    healthy_size = faker.pyint(max_value=healthcheck.DEFAULT_MAX_DISK_SIZE_GB)
    healthcheck.get_directory_size_gb = MagicMock(return_value=healthy_size)
    healthcheck()


@pytest.mark.xfail(reason="work in progress")
def test_disk_unhealthy(faker):
    healthcheck = DiskSpaceAvailable(faker.file_path())
    unhealthy_size = healthcheck.DEFAULT_MAX_DISK_SIZE_GB
    healthcheck.get_directory_size_gb = MagicMock(return_value=unhealthy_size)

    with pytest.raises(HealthCheckFailedError):
        healthcheck()


def test_get_directory_size(faker, fs):
    file_path = faker.file_path()
    size = faker.pyint()
    fs.create_file(file_path, st_size=size)

    healthcheck = DiskSpaceAvailable(os.path.dirname(file_path))
    assert healthcheck.get_directory_size() == size
