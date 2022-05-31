from __future__ import annotations

from pytest_celery.test_services.result_backends.base import ResultBackend
from pytest_celery.test_services.result_backends.rabbitmq import RabbitMQResultBackend
from pytest_celery.test_services.result_backends.redis import RedisResultBackend

__all__ = ("ResultBackend", "RedisResultBackend", "RabbitMQResultBackend")
