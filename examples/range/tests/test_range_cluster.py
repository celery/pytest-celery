import pytest
from pytest_docker_tools import build
from pytest_docker_tools import container
from pytest_docker_tools import fxtr
from pytest_subtests import SubTests

from pytest_celery import DEFAULT_WORKER_CONTAINER_TIMEOUT
from pytest_celery import DEFAULT_WORKER_VOLUME
from pytest_celery import WORKER_DOCKERFILE_ROOTDIR
from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerCluster
from pytest_celery import CeleryWorkerContainer
from tests.conftest import get_celery_versions

versions_range = get_celery_versions("v5.0.0", "v5.0.5")
versions_list = ["v4.4.7", "v5.2.7", "v5.3.0"]


def generate_workers(versions: list[str]) -> list[str]:
    worker_containers = list()
    for v in versions:
        img = f"worker_v{v.replace('.', '_')}_image"
        globals()[img] = build(
            path=WORKER_DOCKERFILE_ROOTDIR,
            tag=f"pytest-celery/examples/worker:v{v}",
            buildargs={
                "CELERY_VERSION": v,
                "CELERY_LOG_LEVEL": fxtr("default_worker_celery_log_level"),
                "CELERY_WORKER_NAME": fxtr("default_worker_celery_worker_name"),
                "CELERY_WORKER_QUEUE": fxtr("default_worker_celery_worker_queue"),
            },
        )
        cnt = f"worker_v{v.replace('.', '_')}_container"
        globals()[cnt] = container(
            image="{" + f"{img}.id" + "}",
            environment=fxtr("default_worker_env"),
            network="{default_pytest_celery_network.name}",
            volumes={"{default_worker_volume.name}": DEFAULT_WORKER_VOLUME},
            wrapper_class=CeleryWorkerContainer,
            timeout=DEFAULT_WORKER_CONTAINER_TIMEOUT,
        )
        worker_containers.append(cnt)
    return worker_containers


class TestClusterList:
    @pytest.fixture(params=[generate_workers(versions_list)])
    def celery_worker_cluster(self, request: pytest.FixtureRequest) -> CeleryWorkerCluster:
        nodes: list[CeleryWorkerContainer] = [request.getfixturevalue(worker) for worker in request.param]
        cluster = CeleryWorkerCluster(*nodes)
        yield cluster
        cluster.teardown()

    def test_worker_cluster_with_fixed_list(self, celery_setup: CeleryTestSetup, subtests: SubTests):
        worker: CeleryTestWorker
        for version, worker in zip(versions_list, celery_setup.worker_cluster):
            with subtests.test(msg=f"Found worker {version} in cluster"):
                assert f"{worker.hostname()} {version}" in worker.logs()


class TestClusterRange:
    @pytest.fixture(params=[generate_workers(versions_range)])
    def celery_worker_cluster(self, request: pytest.FixtureRequest) -> CeleryWorkerCluster:
        nodes: list[CeleryWorkerContainer] = [request.getfixturevalue(worker) for worker in request.param]
        cluster = CeleryWorkerCluster(*nodes)
        yield cluster
        cluster.teardown()

    def test_worker_cluster_with_versions_range(self, celery_setup: CeleryTestSetup, subtests: SubTests):
        worker: CeleryTestWorker
        for version, worker in zip(versions_range, celery_setup.worker_cluster):
            with subtests.test(msg=f"Found worker v{version} in cluster"):
                assert f"{worker.hostname()} v{version}" in worker.logs()
