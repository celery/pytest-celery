from celery import shared_task


@shared_task
def identity(x):
    """Return the argument."""
    return x
