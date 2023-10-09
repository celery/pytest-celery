import gc

from pytest_celery.api.backend import CeleryTestBackend


class RedisTestBackend(CeleryTestBackend):
    def teardown(self) -> None:
        # When a test that has a AsyncResult object is finished
        # there's a race condition between the AsyncResult object
        # and the Redis container. The AsyncResult object tries
        # to release the connection but the Redis container has already
        # exited. This causes a warning to be logged. To avoid this
        # warning we force a garbage collection here.
        gc.collect(1)
        super().teardown()
