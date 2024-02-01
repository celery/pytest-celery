.. _examples_range:

=======
 range
=======

.. contents::
    :local:
    :depth: 2

Description
===========

This example project demonstrates how to mess around with the workers cluster.
It uses a list of Celery versions to create two test configurations:

1. Running against each Celery worker by itself.
2. Running against a cluster of all Celery workers.

It demonste the flexibility of the library, and how you might use it to test your own code.

.. note::
    Testing different worker versions one by one or in a cluster is useful for testing migrations
    and compatibility between different versions. It can be used to define test suites that can verify
    a migration is working as expected, or that a new version is compatible with the old one, etc.

Breakdown
=========

File Structure
~~~~~~~~~~~~~~

The following diagram lists the relevant files in the project.

.. code-block:: text

    range/
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py
    │   └── test_range.py
    │   └── test_range_cluster.py
    └── requirements.txt

conftest.py
~~~~~~~~~~~

We've created a helper function that will return a list of Celery versions that are between two given versions.
It uses the `pypi.org <https://pypi.org/>`_ API to get the list of versions and filters them by the given range.

.. code-block:: python

    def get_celery_versions(start_version: str, end_version: str) -> list[str]:
        url = "https://pypi.org/pypi/celery/json"
        response = requests.get(url)
        data = response.json()
        all_versions = data["releases"].keys()

        filtered_versions = [
            v
            for v in all_versions
            if (
                parse_version(start_version) <= parse_version(v) <= parse_version(end_version)
                and not parse_version(v).is_prerelease
            )
        ]

        return sorted(filtered_versions, key=parse_version)

test_range.py
~~~~~~~~~~~~~

In this scenario, we reconfigure the :func:`default worker <pytest_celery.vendors.worker.fixtures.celery_setup_worker>`
to run against each Celery version in the list. This will add additional `parametization <https://docs.pytest.org/en/latest/how-to/parametrize.html>`_
to the worker fixture, and will generate a different worker for each Celery version.

.. code-block:: python

    class TestRange:
    @pytest.fixture(scope="session", params=get_celery_versions("v4.4.7", "v5.0.0"))
    def celery_version(self, request: pytest.FixtureRequest) -> str:
        return request.param

Following up with this simple test case will produce a test run for each Celery version in the list.

.. code-block:: python

    def test_ping(self, celery_setup: CeleryTestSetup, celery_version: str):
        sig: Signature = ping.s()
        res: AsyncResult = sig.apply_async()
        assert res.get(timeout=RESULT_TIMEOUT) == "pong"

.. note::
    When using `pytest-xdist <https://pypi.org/project/pytest-xdist/>`_ to run tests in parallel, this will
    create a test run for each Celery version in the list, in parallel.

    .. code-block:: text

        tests/test_range.py::TestRange::test_ping[4.4.7-celery_setup_worker-celery_redis_broker-celery_redis_backend]
        tests/test_range.py::TestRange::test_ping[5.0.0-celery_setup_worker-celery_redis_broker-celery_redis_backend]
        tests/test_range.py::TestRange::test_ping[4.4.7-celery_setup_worker-celery_rabbitmq_broker-celery_redis_backend]
        tests/test_range.py::TestRange::test_ping[5.0.0-celery_setup_worker-celery_rabbitmq_broker-celery_redis_backend]

    Notice how it still runs against all the brokers and backends, as we running against default settings.

test_range_cluster.py
~~~~~~~~~~~~~~~~~~~~~

In this scenario, we generate a list of workers per version, and then configure the
:func:`celery_worker_cluster <pytest_celery.fixtures.worker.celery_worker_cluster>` to include all of them.

Once using a range of Celery versions, and once using a fixed list.

.. code-block:: python

    versions_range = get_celery_versions("v5.0.0", "v5.0.5")
    versions_list = ["v4.4.7", "v5.2.7", "v5.3.0"]

The ``generate_workers`` is a helper function that builds worker containers on the fly using the
APIs from `pytest-docker-tools <https://pypi.org/project/pytest-docker-tools/>`_.
Our focus should be on the ``worker_containers`` list, which will contain the names of the generated worker containers fixtures.

.. code-block:: python

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

Next, we configure the :func:`celery_worker_cluster <pytest_celery.fixtures.worker.celery_worker_cluster>`
to include all the workers, and then run a simple test case to verify the cluster is configured as expected.

.. code-block:: python

    class TestClusterList:
        @pytest.fixture(params=[generate_workers(versions_list)])
        def celery_worker_cluster(self, request: pytest.FixtureRequest) -> CeleryWorkerCluster:
            nodes: list[CeleryWorkerContainer] = [request.getfixturevalue(worker) for worker in request.param]
            cluster = CeleryWorkerCluster(*nodes)
            yield cluster
            cluster.teardown()

        def test_worker_cluster_with_fixed_list(self, celery_setup: CeleryTestSetup, subtests):
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

        def test_worker_cluster_with_versions_range(self, celery_setup: CeleryTestSetup, subtests):
            worker: CeleryTestWorker
            for version, worker in zip(versions_range, celery_setup.worker_cluster):
                with subtests.test(msg=f"Found worker v{version} in cluster"):
                    assert f"{worker.hostname()} v{version}" in worker.logs()

Running everything in parallel will produce the following output:

.. code-block:: text

    PASSED tests/test_range.py::TestRange::test_ping[5.0.0-celery_setup_worker-celery_redis_broker-celery_redis_backend]
    PASSED tests/test_range.py::TestRange::test_ping[4.4.7-celery_setup_worker-celery_redis_broker-celery_redis_backend]
    PASSED tests/test_range.py::TestRange::test_ping[4.4.7-celery_setup_worker-celery_rabbitmq_broker-celery_redis_backend]
    PASSED tests/test_range.py::TestRange::test_ping[5.0.0-celery_setup_worker-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v4.4.7 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterList::test_worker_cluster_with_fixed_list[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v4.4.7 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterList::test_worker_cluster_with_fixed_list[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v5.2.7 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterList::test_worker_cluster_with_fixed_list[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v5.2.7 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterList::test_worker_cluster_with_fixed_list[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v5.3.0 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterList::test_worker_cluster_with_fixed_list[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v5.3.0 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterList::test_worker_cluster_with_fixed_list[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    PASSED tests/test_range_cluster.py::TestClusterList::test_worker_cluster_with_fixed_list[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    PASSED tests/test_range_cluster.py::TestClusterList::test_worker_cluster_with_fixed_list[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v5.0.0 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v5.0.1 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v5.0.2 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v5.0.3 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v5.0.4 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v5.0.5 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    PASSED tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_redis_broker-celery_redis_backend]
    [Found worker v5.0.0 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v5.0.1 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v5.0.2 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v5.0.3 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v5.0.4 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    [Found worker v5.0.5 in cluster] SUBPASS tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
    PASSED tests/test_range_cluster.py::TestClusterRange::test_worker_cluster_with_versions_range[celery_worker_cluster0-celery_rabbitmq_broker-celery_redis_backend]
