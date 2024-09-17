import os

import pytest
from celery import Celery

from pytest_celery import LOCALSTACK_CREDS


@pytest.fixture
def default_worker_tasks(default_worker_tasks: set) -> set:
    from tests import tasks

    default_worker_tasks.add(tasks)
    return default_worker_tasks


@pytest.fixture
def default_worker_env(default_worker_env: dict) -> dict:
    default_worker_env.update(LOCALSTACK_CREDS)
    return default_worker_env


@pytest.fixture(scope="session", autouse=True)
def set_aws_credentials():
    os.environ.update(LOCALSTACK_CREDS)


@pytest.fixture
def default_worker_app(default_worker_app: Celery) -> Celery:
    app = default_worker_app
    if app.conf.broker_url and app.conf.broker_url.startswith("sqs"):
        app.conf.broker_transport_options["region"] = LOCALSTACK_CREDS["AWS_DEFAULT_REGION"]
    return app
