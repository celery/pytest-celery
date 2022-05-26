def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "messagebroker: Define one or more message brokers for Celery to use. The "
        "test will run in parallel on each broker.",
    )
    config.addinivalue_line(
        "markers",
        "resultbackend: Define one or more message backends for Celery to use. The "
        "test will run in parallel on each backend.",
    )
