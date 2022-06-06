import uuid

from pytest_celery.contrib.pytest import (
    celery_app,
    celery_includes,
    celery_parameters,
    celery_worker,
    celery_worker_parameters,
    celery_worker_pool,
    use_celery_app_trap,
)
from pytest_celery.fixtures import app, celery_config, celery_enable_logging, manager, message_broker, result_backend
from pytest_celery.test_services.message_brokers import MessageBroker

__all__ = (
    "message_broker",
    "result_backend",
    "manager",
    "app",
    "celery_app",
    "celery_config",
    "celery_parameters",
    "celery_worker",
    "celery_enable_logging",
    "celery_enable_logging",
    "celery_includes",
    "celery_worker_pool",
    "celery_worker_parameters",
)

from pytest_celery.test_services.result_backends import ResultBackend


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
    config.addinivalue_line(
        "markers",
        "celery: Define celery marker. The test will use passed backend and passed broker.",
    )


def pytest_generate_tests(metafunc):
    argvalues = []
    ids = []
    for message_broker_marker in metafunc.definition.iter_markers("messagebroker"):
        for result_backend_marker in metafunc.definition.iter_markers("resultbackend"):
            test_session_id = uuid.uuid4()
            message_broker = message_broker_marker.args[0](test_session_id, *message_broker_marker.args[1:],
                                                           **message_broker_marker.kwargs)

            result_backend = result_backend_marker.args[0](test_session_id, *result_backend_marker.args[1:],
                                                           **result_backend_marker.kwargs)
            ids.append((message_broker.__class__.__name__, result_backend.__class__.__name__))
            argvalues.append((message_broker, result_backend))

    metafunc.parametrize("message_broker,result_backend", argvalues=argvalues, indirect=True)