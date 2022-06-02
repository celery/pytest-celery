import pytest


@pytest.fixture
def message_broker(request):
    with request.param as broker:
        yield broker


@pytest.fixture
def result_backend(request):
    with request.param as backend:
        yield backend
