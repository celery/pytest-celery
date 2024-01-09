from celery import shared_task


@shared_task
def ping() -> str:
    """Pytest-celery internal task.

    Used to check if the worker is up and running.
    """
    return "pong"
