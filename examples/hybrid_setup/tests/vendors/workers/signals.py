from __future__ import annotations

from celery.signals import worker_init


@worker_init.connect
def worker_init_handler(sender, **kwargs):
    print("Worker init handler called!")
