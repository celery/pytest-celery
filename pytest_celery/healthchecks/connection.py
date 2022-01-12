import socket

from pytest_celery.healthchecks import HealthCheck, HealthCheckFailedError

TIMEOUT = 1


class ConnectionHealthy(HealthCheck):

    def __init__(self, endpoint: str, port: int):
        self.endpoint: str = endpoint
        self.port: int = port

    def __call__(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)

        try:
            s.connect((self.endpoint, self.port))
        except (TimeoutError, socket.gaierror, ConnectionError, OSError, TypeError) as e:
            raise HealthCheckFailedError() from e

        try:
            s.close()
        except:
            # TODO: Add debug log here
            pass
