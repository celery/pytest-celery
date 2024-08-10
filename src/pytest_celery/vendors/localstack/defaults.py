"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the Localstack Broker vendor.
"""

CELERY_LOCALSTACK_BROKER = "celery_localstack_broker"
DEFAULT_LOCALSTACK_BROKER = "default_localstack_broker"
LOCALSTACK_IMAGE = "localstack/localstack"
LOCALSTACK_PORTS = {"4566/tcp": None}
LOCALSTACK_CREDS: dict = {
    "AWS_DEFAULT_REGION": "us-east-1",
    "AWS_ACCESS_KEY_ID": "test",
    "AWS_SECRET_ACCESS_KEY": "test",
}
LOCALSTACK_ENV: dict = {
    **LOCALSTACK_CREDS,
}
LOCALSTACK_CONTAINER_TIMEOUT = 60
LOCALSTACK_PREFIX = "sqs://"
