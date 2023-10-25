from unittest.mock import Mock
from unittest.mock import patch

import pytest
import pytest_docker_tools
from celery import Celery

from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryTestNode
from tests.unit.conftest import mocked_container


@pytest.fixture
def mocked_test_container() -> CeleryTestContainer:
    return mocked_container(CeleryTestContainer)


class test_celery_test_node:
    @pytest.fixture
    def node(self, mocked_test_container: CeleryTestContainer):
        return CeleryTestNode(mocked_test_container)

    class test_constructor:
        def test_app(self, mocked_test_container: CeleryTestContainer):
            expected_app = Celery()
            node = CeleryTestNode(mocked_test_container, expected_app)
            assert node.app is expected_app

        def test_eq_opertor_eq(self, mocked_test_container: CeleryTestContainer):
            node1 = CeleryTestNode(mocked_test_container)
            node2 = CeleryTestNode(mocked_test_container)
            assert node1 == node2
            assert node1 is not node2

        def test_eq_opertor_not_eq(self, mocked_test_container: CeleryTestContainer):
            node1 = CeleryTestNode(mocked_test_container)
            node2 = CeleryTestNode(mocked_container(CeleryTestContainer))
            assert node1 != node2
            assert node1 is not node2

    def test_container(self, node: CeleryTestNode):
        assert node.container is not None

    def test_app(self, node: CeleryTestNode):
        assert node.app is None

    def test_default_config(self, node: CeleryTestNode):
        assert node.default_config() == dict()

    def test_ready(self, node: CeleryTestNode):
        assert node.ready()

    def test_config(self, node: CeleryTestNode):
        assert node.config()

    def test_logs(self, node: CeleryTestNode):
        assert node.logs()

    def test_name(self, node: CeleryTestNode):
        assert node.name()

    def test_hostname(self, node: CeleryTestNode):
        assert node.hostname()

    def test_kill(self, node: CeleryTestNode):
        node.kill()

    def test_restart(self, node: CeleryTestNode):
        node.restart()

    def test_teardown(self, node: CeleryTestNode):
        node.teardown()

    def test_wait_for_log(self, node: CeleryTestNode):
        node.wait_for_log("", "test_celey_test_worker.test_wait_for_log")

    def test_assert_log_exists(self, node: CeleryTestNode):
        node.assert_log_exists("", "test_celey_test_worker.test_assert_log_exists")

    def test_assert_log_exists_assertion_error(self, node: CeleryTestNode):
        with patch("pytest_celery.api.base.wait_for_callable", new=Mock()) as mocked_wait_for_callable:
            mocked_wait_for_callable.side_effect = pytest_docker_tools.exceptions.TimeoutError
            with pytest.raises(AssertionError):
                node.assert_log_exists("", "test_celey_test_worker.test_assert_log_exists_assertion_error")

    def test_assert_log_does_not_exist(self, node: CeleryTestNode):
        with patch("pytest_celery.api.base.wait_for_callable", new=Mock()) as mocked_wait_for_callable:
            mocked_wait_for_callable.side_effect = pytest_docker_tools.exceptions.TimeoutError
            node.assert_log_does_not_exist("", "test_celey_test_worker.test_assert_log_does_not_exist")

    def test_assert_log_does_not_exist_assertion_error(self, node: CeleryTestNode):
        with pytest.raises(AssertionError):
            node.assert_log_does_not_exist("", "test_celey_test_worker.test_assert_log_does_not_exist_assertion_error")


class test_celery_test_cluster:
    @pytest.fixture
    def cluster(self, mocked_test_container: CeleryTestContainer):
        local_test_container = mocked_container(CeleryTestContainer)
        node1 = CeleryTestNode(mocked_test_container)
        node2 = CeleryTestNode(local_test_container)
        return CeleryTestCluster(node1, node2)

    class test_constructor:
        def test_set_nodes(self, mocked_test_container: CeleryTestContainer):
            node1 = CeleryTestNode(mocked_test_container)
            node2 = CeleryTestNode(mocked_test_container)
            cluster = CeleryTestCluster(node1)
            cluster._set_nodes(node2)
            assert cluster[0] == node2

        def test_iter(self, mocked_test_container: CeleryTestContainer):
            node1 = CeleryTestNode(mocked_test_container)
            cluster = CeleryTestCluster(node1)
            assert list(cluster) == [node1]

        def test_len(self, mocked_test_container: CeleryTestContainer):
            node1 = CeleryTestNode(mocked_test_container)
            cluster = CeleryTestCluster(node1)
            assert len(cluster) == 1

        def test_getitem(self, mocked_test_container: CeleryTestContainer):
            node1 = CeleryTestNode(mocked_test_container)
            cluster = CeleryTestCluster(node1)
            assert cluster[0] == node1

    def test_nodes_getter(self, cluster: CeleryTestCluster):
        assert cluster.nodes

    def test_nodes_setter(self, cluster: CeleryTestCluster, mocked_test_container: CeleryTestContainer):
        cluster.nodes = cluster.nodes + (mocked_test_container,)
        assert cluster.nodes[-1].container == mocked_test_container
        cluster.nodes = (mocked_test_container,)
        assert cluster[0].container == mocked_test_container

    def test_default_config(self, cluster: CeleryTestCluster):
        assert cluster.default_config() == dict()

    def test_ready(self, cluster: CeleryTestCluster):
        assert cluster.ready()

    def test_config(self, cluster: CeleryTestCluster):
        assert cluster.config()

    def test_teardown(self, cluster: CeleryTestCluster):
        cluster.teardown()
