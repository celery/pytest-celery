from __future__ import annotations

import inspect
import uuid
from collections import Counter

from _pytest.mark import Mark
from _pytest.python import Metafunc

from pytest_celery.fixtures import message_broker  # noqa
from pytest_celery.test_services.message_brokers import MessageBroker

test_groups = Counter()


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


def pytest_generate_tests(metafunc: Metafunc) -> None:
    # todo parametrize nodes, not messagebrokers - something like:
    # message_broker.super().to_node().vhost()
    test_session_id = uuid.uuid4()
    message_brokers: list[MessageBroker] = [
        marker.args[0](test_session_id, *marker.args[1:], **marker.kwargs)
        for marker in metafunc.definition.iter_markers("messagebroker")
    ]
    message_brokers_repr = [repr(b) for b in message_brokers]
    metafunc.parametrize(
        "message_broker",
        indirect=["message_broker"],
        argvalues=message_brokers,
        ids=message_brokers_repr,
    )

    test_groups.update(message_brokers_repr)

    for call in metafunc._calls:
        test_group = test_groups[repr(call.params["message_broker"])]
        call.marks.append(Mark("order", (test_group,), {}))

    if "message_broker" not in metafunc.fixturenames:
        raise TypeError()

    # TODO: Check if msg brokers are duplicates and compare configurations before deciding
    # if len(message_broker_markers) != len(set(message_broker_markers)):
    #     raise ValueError(f"Bla bla. use n={len(message_broker_markers)}")
