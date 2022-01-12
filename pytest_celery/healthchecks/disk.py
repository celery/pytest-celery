from pathlib import Path

from pytest_celery.healthchecks import DiskSpaceUnavailableError, HealthCheck, HealthCheckFailedError


def to_gb(size_in_bytes: int) -> float:
    size_in_bytes * 1e-9


class DiskSpaceAvailable(HealthCheck):
    DEFAULT_MAX_DISK_SIZE_GB = 2
    DEFAULT_MAX_PERCENTAGE = 0.8

    def __init__(
        self,
        path_to_disk: str,
        max_disk_size_gb: int = DEFAULT_MAX_DISK_SIZE_GB,
        max_percentage: float = DEFAULT_MAX_PERCENTAGE,
    ):
        self.path_to_disk: str = path_to_disk
        self.max_disk_size_gb: int = max_disk_size_gb
        self.max_percentage: float = max_percentage
        self.max_healthy_size: int = self.max_disk_size_gb * self.max_percentage

    def __call__(self) -> None:
        try:
            directory_size = to_gb(self.get_directory_size())
            if directory_size > self.max_healthy_size:
                raise DiskSpaceUnavailableError(
                    self.path_to_disk, directory_size, self.max_disk_size_gb, self.max_healthy_size
                )

        except (ValueError, NotImplementedError) as e:
            raise HealthCheckFailedError() from e

    def get_directory_size(self) -> float:
        return sum(p.stat().st_size for p in Path(self.path_to_disk).rglob("*"))
