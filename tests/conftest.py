import os

import docker
import pytest
from celery import Celery

from pytest_celery import ALL_CELERY_BROKERS
from pytest_celery import CELERY_LOCALSTACK_BROKER
from pytest_celery import LOCALSTACK_CREDS
from pytest_celery import CeleryTestBroker
from pytest_celery import _is_vendor_installed

if _is_vendor_installed("localstack"):
    ALL_CELERY_BROKERS.add(CELERY_LOCALSTACK_BROKER)


@pytest.fixture(params=ALL_CELERY_BROKERS)
def celery_broker(request: pytest.FixtureRequest) -> CeleryTestBroker:  # type: ignore
    broker: CeleryTestBroker = request.getfixturevalue(request.param)
    yield broker
    broker.teardown()


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


@pytest.fixture(scope="module", autouse=True)
def auto_clean_docker_resources():
    """Clean up Docker resources after each test module."""
    # Used for debugging
    verbose = False

    def log(message):
        if verbose:
            print(message)

    def cleanup_docker_resources():
        """Function to clean up Docker containers, networks, and volumes based
        on labels."""
        docker_client = docker.from_env()

        try:
            # Clean up containers with the label 'creator=pytest-docker-tools'
            containers = docker_client.containers.list(all=True, filters={"label": "creator=pytest-docker-tools"})
            for con in containers:
                con.reload()  # Ensure we have the latest status
                if con.status != "running":  # Only remove non-running containers
                    log(f"Removing container {con.name}")
                    con.remove(force=True)
                else:
                    log(f"Skipping running container {con.name}")

            # Clean up networks with names starting with 'pytest-'
            networks = docker_client.networks.list(names=["pytest-*"])
            for network in networks:
                if not network.containers:  # Check if the network is in use
                    log(f"Removing network {network.name}")
                    network.remove()
                else:
                    log(f"Skipping network {network.name}, still in use")

            # Clean up volumes with names starting with 'pytest-*'
            volumes = docker_client.volumes.list(filters={"name": "pytest-*"})
            for volume in volumes:
                if not volume.attrs.get("UsageData", {}).get("RefCount", 0):  # Check if volume is not in use
                    log(f"Removing volume {volume.name}")
                    volume.remove()
                else:
                    log(f"Skipping volume {volume.name}, still in use")

        except Exception as e:
            log(f"Error occurred while cleaning up Docker resources: {e}")

    log("--- Running Docker resource cleanup ---")
    cleanup_docker_resources()
