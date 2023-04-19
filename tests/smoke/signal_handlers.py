from celery.signals import worker_init
from celery.signals import worker_process_init
from celery.signals import worker_process_shutdown
from celery.signals import worker_ready
from celery.signals import worker_shutdown


@worker_init.connect
def worker_init_handler(sender, **kwargs):  # type: ignore
    print("worker_init_handler")


@worker_process_init.connect
def worker_process_init_handler(sender, **kwargs):  # type: ignore
    print("worker_process_init_handler")


@worker_process_shutdown.connect
def worker_process_shutdown_handler(sender, pid, exitcode, **kwargs):  # type: ignore
    print("worker_process_shutdown_handler")


@worker_ready.connect
def worker_ready_handler(sender, **kwargs):  # type: ignore
    print("worker_ready_handler")


@worker_shutdown.connect
def worker_shutdown_handler(sender, **kwargs):  # type: ignore
    print("worker_shutdown_handler")
