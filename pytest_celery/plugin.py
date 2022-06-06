import uuid

from pytest_celery.fixtures import message_broker, result_backend, manager, app, celery_config, celery_enable_logging
from pytest_celery.contrib.pytest import celery_app, celery_parameters, celery_worker, use_celery_app_trap, celery_includes, celery_worker_pool, celery_worker_parameters
from pytest_celery.test_services.message_brokers import MessageBroker

__all__ = ("message_broker", "result_backend", "manager", "app", "celery_app", "celery_config", "celery_parameters", "celery_worker",
           "celery_enable_logging", "celery_enable_logging", "celery_includes", "celery_worker_pool", "celery_worker_parameters")

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


def parametrize_message_broker(metafunc):
    message_broker_markers = [marker.args[0] for marker in metafunc.definition.iter_markers("messagebroker")]

    if not message_broker_markers:
        return

    test_session_id = uuid.uuid4()
    message_brokers: list[MessageBroker] = [
        marker.args[0](test_session_id, *marker.args[1:], **marker.kwargs)
        for marker in metafunc.definition.iter_markers("messagebroker")
    ]

    message_brokers_ids = [result_backend.__class__.__name__ for result_backend in message_brokers]

    metafunc.parametrize("message_broker", argvalues=message_brokers, indirect=True, ids=message_brokers_ids)


def parametrize_result_backend(metafunc):
    result_backend_markers = [marker.args[0] for marker in metafunc.definition.iter_markers("resultbackend")]

    if not result_backend_markers:
        return

    test_session_id = uuid.uuid4()
    result_backends: list[ResultBackend] = [
        marker.args[0](test_session_id, *marker.args[1:], **marker.kwargs)
        for marker in metafunc.definition.iter_markers("resultbackend")
    ]

    result_backends_ids = [result_backend.__class__.__name__ for result_backend in result_backends]

    metafunc.parametrize("result_backend", argvalues=result_backends, indirect=True, ids=result_backends_ids)


# def parametrize_celery(metafunc):
#     celery_markers = [marker.args for marker in metafunc.definition.iter_markers("celery")]
#     if len(celery_markers) == 0:
#         return
#
#     argvalues = celery_markers[0]
#     if len(argvalues) == 0:
#         argvalues = {"main": "celery.tests"}
#     metafunc.parametrize("app", argvalues=[argvalues], indirect=True)


def pytest_generate_tests(metafunc):
    parametrize_message_broker(metafunc)
    parametrize_result_backend(metafunc)
    # parametrize_celery(metafunc)
