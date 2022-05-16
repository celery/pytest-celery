import pytest
from redis import Redis

from pytest_celery.test_services.message_brokers.redis import RedisBroker


@pytest.mark.parametrize(
    "url",
    [
        "redis://localhost:2222",
        "redis://user@localhost:2222",
        "redis://:123@localhost:2222",
        "redis://user:1234@localhost:2222",
    ],
)
def test_redis_broker_url(container, test_session_id, url):
    container.get_client.return_value = Redis.from_url(url)
    rb = RedisBroker(test_session_id, container=container)

    assert rb.url == url


@pytest.mark.parametrize("url", ["redis:", "redis://"])
def test_redis_broker_url_only_with_schema(container, test_session_id, url):
    container.get_client.return_value = Redis.from_url(url)
    rb = RedisBroker(test_session_id, container=container)

    assert rb.url in ["redis:", "redis://"]
