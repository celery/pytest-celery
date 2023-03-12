import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import defaults
from pytest_celery.components.backend.redis.api import RedisTestBackend
from pytest_celery.components.broker.rabbitmq.api import RabbitMQTestBroker
from pytest_celery.components.containers.rabbitmq import RabbitMQContainer
from pytest_celery.components.containers.redis import RedisContainer


class test_redis_container_settings:
    @pytest.mark.parametrize(
        "container, expected_image, expected_ports",
        [
            (
                lazy_fixture(defaults.REDIS_SESSION_BACKEND),
                defaults.REDIS_SESSION_BACKEND_IMAGE,
                defaults.REDIS_SESSION_BACKEND_PORTS,
            ),
            (
                lazy_fixture(defaults.REDIS_FUNCTION_BACKEND),
                defaults.REDIS_FUNCTION_BACKEND_IMAGE,
                defaults.REDIS_FUNCTION_BACKEND_PORTS,
            ),
            (
                lazy_fixture(defaults.REDIS_FUNCTION_BROKER),
                defaults.REDIS_SESSION_BACKEND_IMAGE,
                defaults.REDIS_SESSION_BACKEND_PORTS,
            ),
            (
                lazy_fixture(defaults.REDIS_SESSION_BROKER),
                defaults.REDIS_FUNCTION_BROKER_IMAGE,
                defaults.REDIS_FUNCTION_BROKER_PORTS,
            ),
            (
                lazy_fixture(defaults.REDIS_SESSION_BROKER),
                defaults.REDIS_SESSION_BROKER_IMAGE,
                defaults.REDIS_SESSION_BROKER_PORTS,
            ),
        ],
    )
    def test_defaults(self, container: RedisContainer, expected_image: str, expected_ports: dict):
        attrs = container.attrs
        assert attrs["Config"]["Image"] == expected_image
        assert attrs["Config"]["ExposedPorts"].keys() == expected_ports.keys()

    def test_celery_redis_backend_default_config(
        self,
        celery_redis_backend: RedisTestBackend,
        redis_function_backend: RedisContainer,
        redis_session_backend: RedisContainer,
    ):
        assert celery_redis_backend.container.attrs != redis_function_backend.attrs
        assert celery_redis_backend.container.attrs == redis_session_backend.attrs


class test_rabbitmq_container_settings:
    @pytest.mark.parametrize(
        "container, expected_image",
        [
            (
                lazy_fixture(defaults.RABBITMQ_FUNCTION_BROKER),
                defaults.RABBITMQ_FUNCTION_BROKER_IMAGE,
            ),
            (
                lazy_fixture(defaults.RABBITMQ_SESSION_BROKER),
                defaults.RABBITMQ_SESSION_BROKER_IMAGE,
            ),
        ],
    )
    def test_defaults(self, container: RabbitMQContainer, expected_image: str):
        attrs = container.attrs
        assert attrs["Config"]["Image"] == expected_image

    def test_celery_rabbitmq_broker_default_config(
        self,
        celery_rabbitmq_broker: RabbitMQTestBroker,
        rabbitmq_function_broker: RabbitMQContainer,
        rabbitmq_session_broker: RabbitMQContainer,
    ):
        assert celery_rabbitmq_broker.container.attrs != rabbitmq_function_broker.attrs
        assert celery_rabbitmq_broker.container.attrs == rabbitmq_session_broker.attrs
