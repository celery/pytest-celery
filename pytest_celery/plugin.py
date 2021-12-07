def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "messagebroker: Define one or more message brokers for Celery to use. The "
        "test will run in parallel on each broker.",
    )


seen_tests = set()


def pytest_generate_tests(metafunc):
    message_broker_markers = [marker.args[0] for marker in metafunc.definition.iter_markers("messagebroker")]

    if message_broker_markers:
        if len(message_broker_markers) != len(set(message_broker_markers)):
            raise ValueError(f"Bla bla. use n={len(message_broker_markers)}")

        metafunc.parametrize("broker_type", message_broker_markers, indirect=True)
        for call in metafunc._calls:
            call.marks = []


# def pytest_configure_message_broker(config, message_broker):
#     pass
