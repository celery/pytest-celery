""" Template for Celery worker application. """
from __future__ import annotations

import json
import logging
import sys

from celery import Celery
from celery.signals import after_setup_logger

imports = None

app = Celery("celery_test_app")
config = None

if config:
    app.config_from_object(config)
    print(f"Changed worker configuration: {json.dumps(config, indent=4)}")


@after_setup_logger.connect
def setup_loggers(logger: logging.Logger, *args: tuple, **kwargs: dict) -> None:
    # https://distributedpython.com/posts/celery-docker-and-the-missing-startup-banner/
    logger.addHandler(logging.StreamHandler(sys.stdout))


if __name__ == "__main__":
    app.start()
