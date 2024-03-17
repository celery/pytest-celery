import celery.utils
from celery import shared_task
from celery.canvas import group

from pytest_celery import RESULT_TIMEOUT


@shared_task
def noop(*args, **kwargs) -> None:
    return celery.utils.noop(*args, **kwargs)


@shared_task
def identity(x):
    return x


@shared_task
def job() -> str:
    canvas = (
        group(
            identity.si("Hello, "),
            identity.si("world!"),
        )
        | noop.s().set(queue="legacy")
        | identity.si("Done!")
    )
    return canvas.delay().get(timeout=RESULT_TIMEOUT)
