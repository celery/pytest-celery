from pytest_celery.fixtures import message_broker

import inspect


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "messagebroker: Define one or more message brokers for Celery to use. The "
        "test will run in parallel on each broker.",
    )


seen_tests = set()


def pytest_pycollect_makeitem(collector, name, obj):
    markers = getattr(obj, 'pytestmark', None)
    has_message_broker_marker = True    # todo

    if inspect.isfunction(obj) and has_message_broker_marker:
        # message_broker_markers = [marker for marker in markers if marker.name == 'messagebroker']
        return list(collector._genfunctions(name, obj))

    return None


def pytest_generate_tests(metafunc):
    message_brokers = [marker.args[0]() for marker in metafunc.definition.iter_markers("messagebroker")]
    metafunc.parametrize("message_broker",
                         indirect=["message_broker"],
                         argvalues=message_brokers,
                         ids=[repr(b) for b in message_brokers])

    if 'message_broker' not in metafunc.fixturenames:
        raise TypeError()

    # TODO: Check if msg brokers are duplicates and compare configurations before deciding
    # if len(message_broker_markers) != len(set(message_broker_markers)):
    #     raise ValueError(f"Bla bla. use n={len(message_broker_markers)}")
