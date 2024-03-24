from celery import Task
from celery import shared_task
from celery import signature
from celery.canvas import Signature

from pytest_celery.vendors.worker.tasks import *  # noqa


@shared_task
def replaced_with_me():
    return True


@shared_task(bind=True)
def replace_with_task(self: Task, replace_with: Signature = None):
    if replace_with is None:
        replace_with = replaced_with_me.s()
    self.replace(signature(replace_with))
