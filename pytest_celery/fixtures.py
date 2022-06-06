from celery import Celery
import pytest


@pytest.fixture
def message_broker(request):
    with request.param as broker:
        yield broker


@pytest.fixture
def result_backend(request):
    with request.param as backend:
        yield backend


@pytest.fixture
def app(request, message_broker, result_backend):
    app = Celery(broker=message_broker.url,
                 backend=result_backend.url, **request.param)
    yield app
