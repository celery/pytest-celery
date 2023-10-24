from unittest.mock import Mock
from unittest.mock import patch

import pytest
from celery import Celery

from pytest_celery import CeleryTestCluster
from pytest_celery import CeleryTestContainer
from pytest_celery import CeleryTestNode


@pytest.fixture
def mocked_test_container() -> CeleryTestContainer:
    return Mock(spec=CeleryTestContainer)


@pytest.fixture(autouse=True)
def mock_wait_for_callable():
    with patch("pytest_celery.api.base.wait_for_callable", new=Mock()):
        yield


class test_celery_test_node:
    @pytest.fixture
    def node(self, mocked_test_container: CeleryTestContainer):
        return CeleryTestNode(mocked_test_container)

    def test_app(self, mocked_test_container: CeleryTestContainer):
        expected_app = Celery()
        node = CeleryTestNode(mocked_test_container, expected_app)
        assert node.app is expected_app

    def test_default_config_format(self, mocked_test_container: CeleryTestContainer):
        node = CeleryTestNode(mocked_test_container)
        assert node.default_config() == dict()

    def test_eq_opertor(self, mocked_test_container: CeleryTestContainer):
        node1 = CeleryTestNode(mocked_test_container)
        node2 = CeleryTestNode(mocked_test_container)
        assert node1 == node2
        assert node1 is not node2

    def test_ready(self, node: CeleryTestNode):
        assert node.ready()

    def test_wait_for_log(self, node: CeleryTestNode):
        node.wait_for_log("", "test_celey_test_worker.test_wait_for_log")

    def test_assert_log_exists(self, node: CeleryTestNode):
        node.assert_log_exists("", "test_celey_test_worker.test_assert_log_exists")


class test_celery_test_cluster:
    @pytest.fixture
    def cluster(self, mocked_test_container: CeleryTestContainer):
        local_test_container = Mock(spec=CeleryTestContainer)
        node1 = CeleryTestNode(mocked_test_container)
        node2 = CeleryTestNode(local_test_container)
        return CeleryTestCluster(node1, node2)

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

    def test_ready(self, cluster: CeleryTestCluster):
        assert cluster.ready()

    def test_default_config_format(self, cluster: CeleryTestCluster):
        assert cluster.default_config() == dict()
