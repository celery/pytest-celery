import pytest


@pytest.fixture
def message_broker(request):
    with request.param:
        yield
