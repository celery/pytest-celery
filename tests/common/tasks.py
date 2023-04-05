from celery import shared_task


@shared_task
def identity(x):
    return x
