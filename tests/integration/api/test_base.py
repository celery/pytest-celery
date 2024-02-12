from __future__ import annotations

import pytest

from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestNode
from pytest_celery import RedisTestBackend


class BaseNodes:
    def test_ready(self, node: CeleryTestNode):
        assert node.ready()

    def test_app(self, node: CeleryTestNode):
        assert node.app is None

    def test_logs(self, node: CeleryTestNode):
        node.logs()

    def test_name(self, node: CeleryTestNode):
        assert isinstance(node.name(), str)

    def test_hostname(self, node: CeleryTestNode):
        hostname = node.hostname()
        assert isinstance(hostname, str)
        assert node.container.id[:12] in hostname

    @pytest.mark.parametrize("signal", [None, "SIGKILL"])
    def test_kill(self, node: CeleryTestNode, signal: str | int):
        node.kill(signal)
        assert node.container.status == "exited"

    def test_kill_no_reload(self, node: CeleryTestNode):
        node.kill(reload_container=False)
        assert node.container.status != "exited"

    @pytest.mark.parametrize("force", [True, False])
    def test_restart(self, node: CeleryTestNode, force: bool):
        node.restart(force=force)
        assert node.container.status == "running"

    def test_restart_no_reload(self, node: CeleryTestNode):
        node.restart(reload_container=False)
        assert node.container.status == "running"

    def test_teardown(self, node: CeleryTestNode):
        if isinstance(node, RedisTestBackend):
            pytest.skip("RedisTestBackend.teardown() breaks the testing environment")
        node.teardown()

    @pytest.mark.skip(reason="TODO")
    def test_wait_for_logs(self, node: CeleryTestNode):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_assert_log_exists(self, node: CeleryTestNode):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_assert_log_does_not_exist(self, node: CeleryTestNode):
        pass


class BaseCluster:
    def test_ready(self, cluster: CeleryTestCluster):
        assert cluster.ready()

    def test_teardown(self, cluster: CeleryTestCluster):
        cluster.teardown()

    def test_app(self, cluster: CeleryTestCluster):
        node: CeleryTestNode
        for node in cluster:
            assert node.app is None

    def test_config(self, cluster: CeleryTestCluster):
        expected_keys = {"urls", "host_urls"}
        assert set(cluster.config().keys()) == expected_keys
