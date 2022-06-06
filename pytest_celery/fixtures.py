import pytest

from pytest_celery.contrib.testing.manager import Manager


@pytest.fixture
def message_broker(request):
    with request.param as broker:
        yield broker


@pytest.fixture
def result_backend(request):
    with request.param as backend:
        yield backend


@pytest.fixture
def celery_config(message_broker, result_backend):
    return {
        "broker_url": message_broker.url,
        "result_backend": result_backend.url,
        "cassandra_servers": ["localhost"],
        "cassandra_keyspace": "tests",
        "cassandra_table": "tests",
        "cassandra_read_consistency": "ONE",
        "cassandra_write_consistency": "ONE",
    }


@pytest.fixture
def celery_enable_logging():
    return True


@pytest.fixture(scope="session")
def celery_worker_pool():
    return "prefork"


@pytest.fixture
def app(celery_app):
    yield celery_app


@pytest.fixture
def manager(app, celery_worker):
    return Manager(app)


@pytest.fixture(autouse=True)
def ZZZZ_set_app_current(app):
    app.set_current()
    app.set_default()
