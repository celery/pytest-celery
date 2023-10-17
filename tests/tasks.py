import time

import celery.utils
from celery import shared_task


@shared_task
def noop(*args, **kwargs) -> None:
    return celery.utils.noop(*args, **kwargs)


@shared_task
def identity(x):
    return x


@shared_task
def sleep(seconds: float = 1, **kwargs) -> True:
    time.sleep(seconds, **kwargs)
    return True


@shared_task
def add(x, y):
    return x + y
