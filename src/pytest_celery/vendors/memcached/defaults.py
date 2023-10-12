CELERY_MEMCACHED_BACKEND = "celery_memcached_backend"
DEFAULT_MEMCACHED_BACKEND = "default_memcached_backend"
MEMCACHED_IMAGE = "memcached:latest"
MEMCACHED_PORTS = {"11211/tcp": None}
MEMCACHED_ENV: dict = {}
MEMCACHED_CONTAINER_TIMEOUT = 60
