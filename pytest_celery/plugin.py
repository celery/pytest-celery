import uuid

from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.fixtures import message_broker, result_backend

__all__ = ("message_broker", "result_backend")

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


def parametrize_message_broker(metafunc):
    message_broker_markers = [marker.args[0] for marker in metafunc.definition.iter_markers("messagebroker")]

    if not message_broker_markers:
        return

    test_session_id = uuid.uuid4()
    message_brokers: list[MessageBroker] = [
        marker.args[0](test_session_id, *marker.args[1:], **marker.kwargs)
        for marker in metafunc.definition.iter_markers("messagebroker")
    ]

    metafunc.parametrize(
        "message_broker",
        argvalues=message_brokers,
        indirect=True
    )


def parametrize_result_backend(metafunc):
    result_backend_markers = [marker.args[0] for marker in metafunc.definition.iter_markers("resultbackend")]

    if not result_backend_markers:
        return

    test_session_id = uuid.uuid4()
    result_backends: list[ResultBackend] = [
        marker.args[0](test_session_id, *marker.args[1:], **marker.kwargs)
        for marker in metafunc.definition.iter_markers("resultbackend")
    ]

    metafunc.parametrize(
        "result_backend",
        argvalues=result_backends,
        indirect=True
    )


def pytest_generate_tests(metafunc):
    parametrize_message_broker(metafunc)
    parametrize_result_backend(metafunc)
