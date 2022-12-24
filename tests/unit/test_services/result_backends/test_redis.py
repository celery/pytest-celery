import pytest
from redis import Redis

from pytest_celery.test_services.result_backends import RedisResultBackend


@pytest.mark.parametrize(
    "url",
    [
        "redis://localhost:2222",
        "redis://user@localhost:2222",
        "redis://:123@localhost:2222",
        "redis://user:1234@localhost:2222",
    ],
)
def test_redis_backend_url(container, test_session_id, url, subtests):
    container.get_client.return_value = Redis.from_url(url)
    rb = RedisResultBackend(test_session_id, container=container)

    with subtests.test("Redis URI is identical"):
        assert rb.url == url

    with subtests.test("Debug representation includes original url in full"):
        assert repr(rb) == f"Redis Result Backend <{url}>"


@pytest.mark.skip
@pytest.mark.parametrize("url", ["redis:", "redis://"])
def test_redis_backend_url_only_with_schema(container, test_session_id, url):
    container.get_client.return_value = Redis.from_url(url)
    rb = RedisResultBackend(test_session_id, container=container)

    assert rb.url in ["redis:", "redis://"]
