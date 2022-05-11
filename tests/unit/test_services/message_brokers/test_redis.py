import pytest
from redis import Redis

from pytest_celery.test_services.message_brokers.redis import RedisBroker


@pytest.mark.parametrize("url", ["redis://", "redis://localhost:2222", "redis://user:1234@localhost:2222/0"])
def test_start(container, test_session_id, url):
    container.get_client.return_value = Redis(url)
    rb = RedisBroker(test_session_id, container=container)
    assert rb.url == url
