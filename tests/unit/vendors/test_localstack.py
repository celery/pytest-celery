from __future__ import annotations

import pytest

from pytest_celery import LOCALSTACK_ENV
from pytest_celery import LOCALSTACK_IMAGE
from pytest_celery import LOCALSTACK_PORTS
from pytest_celery import LOCALSTACK_PREFIX
from pytest_celery import LocalstackContainer
from pytest_celery import LocalstackTestBroker


class test_localstack_container:
    def test_version(self):
        assert LocalstackContainer.version() == "localstack"

    def test_env(self):
        assert LocalstackContainer.initial_env() == LOCALSTACK_ENV

    def test_image(self):
        assert LocalstackContainer.image() == LOCALSTACK_IMAGE

    def test_ports(self):
        assert LocalstackContainer.ports() == LOCALSTACK_PORTS

    def test_prefix(self):
        assert LocalstackContainer.prefix() == LOCALSTACK_PREFIX


class test_localstack_broker_api:
    @pytest.mark.skip(reason="Placeholder")
    def test_placeholder(self, celery_localstack_broker: LocalstackTestBroker):
        # The class LocalstackTestBroker is currently a placeholder
        # so we don't have any specific tests for it yet.
        # This test suite is pre-configured to test the LocalstackTestBroker
        # and ready to be used once the class is implemented.
        pass
