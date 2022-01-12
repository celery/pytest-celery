from abc import ABCMeta, abstractmethod


class HealthCheckFailedError(Exception):
    pass


class DiskSpaceUnavailableError(HealthCheckFailedError):
    def __init__(self, path, size_in_gb, max_size_gb, max_healthy_size):
        self.message = "Disk space unavailable: directory {} has {} GB of data. " \
                       "The max size is {} GB, max healthy size is {} GB."\
            .format(path, size_in_gb, max_size_gb, max_healthy_size)
        super().__init__(self.message)


class HealthCheck(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self) -> None:
        pass


