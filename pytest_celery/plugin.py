import uuid

from pytest_celery.fixtures import message_broker, result_backend, app
from pytest_celery.test_services.message_brokers import MessageBroker

__all__ = ("message_broker", "result_backend", "app")

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

    metafunc.parametrize("message_broker", argvalues=message_brokers, indirect=True)


def parametrize_result_backend(metafunc):
    result_backend_markers = [marker.args[0] for marker in metafunc.definition.iter_markers("resultbackend")]

    if not result_backend_markers:
        return

    test_session_id = uuid.uuid4()
    result_backends: list[ResultBackend] = [
        marker.args[0](test_session_id, *marker.args[1:], **marker.kwargs)
        for marker in metafunc.definition.iter_markers("resultbackend")
    ]

    metafunc.parametrize("result_backend", argvalues=result_backends, indirect=True)


def parametrize_celery(metafunc):
    celery_markers = [marker.args for marker in metafunc.definition.iter_markers("celery")]
    if len(celery_markers) == 0:
        return

    argvalues = celery_markers[0]
    if len(argvalues) == 0:
        argvalues = {"main": "celery.tests"}
    metafunc.parametrize("app", argvalues=[argvalues], indirect=True)


def pytest_generate_tests(metafunc):
    parametrize_message_broker(metafunc)
    parametrize_result_backend(metafunc)
    parametrize_celery(metafunc)
