import inspect
import uuid

from pytest_celery.fixtures import message_broker  # noqa


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "messagebroker: Define one or more message brokers for Celery to use. The "
        "test will run in parallel on each broker.",
    )


seen_tests = set()


def pytest_pycollect_makeitem(collector, name, obj):
    markers = getattr(obj, "pytestmark", ())
    has_message_broker_marker = any(
        True for marker in markers if marker.name == "messagebroker"
    )

    if inspect.isfunction(obj) and has_message_broker_marker:
        return list(collector._genfunctions(name, obj))

    return None


def pytest_generate_tests(metafunc):
    # todo parametrize nodes, not messagebrokers - something like:
    # message_broker.super().to_node().vhost()
    test_session_id = uuid.uuid4()
    message_brokers = [
        marker.args[0](test_session_id)
        for marker in metafunc.definition.iter_markers("messagebroker")
    ]
    metafunc.parametrize(
        "message_broker",
        indirect=["message_broker"],
        argvalues=message_brokers,
        ids=[repr(b) for b in message_brokers],
    )

    if "message_broker" not in metafunc.fixturenames:
        raise TypeError()

    # TODO: Check if msg brokers are duplicates and compare configurations before deciding
    # if len(message_broker_markers) != len(set(message_broker_markers)):
    #     raise ValueError(f"Bla bla. use n={len(message_broker_markers)}")
