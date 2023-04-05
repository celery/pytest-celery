from pytest_celery import RedisContainer


class test_redis_container:
    def test_client(self, redis_test_container: RedisContainer):
        assert redis_test_container.client()
