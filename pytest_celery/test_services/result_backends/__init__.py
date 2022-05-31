from __future__ import annotations

from pytest_celery.test_services.result_backends.base import ResultBackend
from pytest_celery.test_services.result_backends.redis import RedisResultBackend
from pytest_celery.test_services.result_backends.rabbitmq import RabbitMQResultBackend

__all__ = ("ResultBackend", "RedisResultBackend", "RabbitMQResultBackend")
