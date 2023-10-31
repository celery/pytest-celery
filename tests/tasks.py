import time

import celery.utils
from celery import Task
from celery import shared_task
from celery import signature
from celery.canvas import Signature


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


@shared_task
def replaced_with_me():
    return True


@shared_task(bind=True)
def replace_with_task(self: Task, replace_with: Signature = None):
    if replace_with is None:
        replace_with = replaced_with_me.s()
    self.replace(signature(replace_with))
