import uuid

from pytest_celery.test_services.message_brokers import MessageBroker


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

    if len(message_broker_markers) != len(set(message_broker_markers)):
        raise ValueError(f"The same message broker defined twice, use n={len(message_broker_markers)} instead")

    test_session_id = uuid.uuid4()
    message_brokers: list[MessageBroker] = [
        marker.args[0](test_session_id, *marker.args[1:], **marker.kwargs)
        for marker in metafunc.definition.iter_markers("messagebroker")
    ]

    for message_broker in message_brokers:
        message_broker.start()

    metafunc.parametrize(
        "message_broker",
        message_brokers,
    )


def parametrize_result_backend(metafunc):
    result_backend_markers = [marker.args[0] for marker in metafunc.definition.iter_markers("resultbackend")]

    if not result_backend_markers:
        return

    if len(result_backend_markers) != len(set(result_backend_markers)):
        raise ValueError(f"The same message broker defined twice, use n={len(result_backend_markers)} instead")

    test_session_id = uuid.uuid4()
    result_backends: list[MessageBroker] = [
        marker.args[0](test_session_id, *marker.args[1:], **marker.kwargs)
        for marker in metafunc.definition.iter_markers("resultbackend")
    ]

    for result_backend in result_backends:
        result_backend.start()

    metafunc.parametrize(
        "result_backend",
        result_backends,
    )

def pytest_generate_tests(metafunc):
    parametrize_message_broker(metafunc)
    parametrize_result_backend(metafunc)


