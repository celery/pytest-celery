from __future__ import annotations

import pytest

from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestNode
from pytest_celery import RedisTestBackend
from tests.defaults import ALL_CLUSTERS_FIXTURES
from tests.defaults import ALL_NODES_FIXTURES


@pytest.mark.parametrize("node", ALL_NODES_FIXTURES)
class test_celery_test_node:
    def test_ready(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        assert node.ready()

    def test_logs(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        node.logs()

    def test_name(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        assert isinstance(node.name(), str)

    def test_hostname(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        hostname = node.hostname()
        assert isinstance(hostname, str)
        assert node.container.id[:12] in hostname

    @pytest.mark.parametrize("signal", [None, "SIGKILL"])
    def test_kill(self, node: CeleryTestNode, signal: str | int, request):
        node = request.getfixturevalue(node)
        node.kill(signal)
        assert node.container.status == "exited"

    def test_kill_no_reload(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        node.kill(reload_container=False)
        assert node.container.status != "exited"

    @pytest.mark.parametrize("force", [True, False])
    def test_restart(self, node: CeleryTestNode, force: bool, request):
        node = request.getfixturevalue(node)
        node.restart(force=force)
        assert node.container.status == "running"

    def test_restart_no_reload(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        node.restart(reload_container=False)
        assert node.container.status == "running"

    def test_teardown(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        if isinstance(node, RedisTestBackend):
            pytest.skip("RedisTestBackend.teardown() breaks the testing environment")
        node.teardown()

    @pytest.mark.skip(reason="TODO")
    def test_wait_for_logs(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        pass

    @pytest.mark.skip(reason="TODO")
    def test_assert_log_exists(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        pass

    @pytest.mark.skip(reason="TODO")
    def test_assert_log_does_not_exist(self, node: CeleryTestNode, request):
        node = request.getfixturevalue(node)
        pass


@pytest.mark.parametrize("cluster", ALL_CLUSTERS_FIXTURES)
class test_celery_test_cluster:
    def test_ready(self, cluster: CeleryTestCluster, request):
        cluster = request.getfixturevalue(cluster)
        assert cluster.ready()

    def test_teardown(self, cluster: CeleryTestCluster, request):
        cluster = request.getfixturevalue(cluster)
        cluster.teardown()
