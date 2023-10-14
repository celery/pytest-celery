import json
import logging
import sys

from celery import Celery
from celery.signals import after_setup_logger

config_updates = None
name = "celery_test_app"  # Default name if not provided by the initial content

# Will be populated accoring to the initial content
{0}
{1}
app = Celery(name)

{2}

if config_updates:
    app.config_from_object(config_updates)
    print(f"Config updates from default_worker_app fixture: {json.dumps(config_updates, indent=4)}")


@after_setup_logger.connect
def setup_loggers(logger: logging.Logger, *args: tuple, **kwargs: dict) -> None:
    # https://distributedpython.com/posts/celery-docker-and-the-missing-startup-banner/
    logger.addHandler(logging.StreamHandler(sys.stdout))


if __name__ == "__main__":
    app.start()
