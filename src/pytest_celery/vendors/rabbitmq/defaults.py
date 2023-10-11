CELERY_RABBITMQ_BROKER = "celery_rabbitmq_broker"
DEFAULT_RABBITMQ_BROKER = "default_rabbitmq_broker"
RABBITMQ_IMAGE = "rabbitmq:latest"
RABBITMQ_PORTS = {"5672/tcp": None}
RABBITMQ_ENV: dict = {}
RABBITMQ_CONTAINER_TIMEOUT = 120
