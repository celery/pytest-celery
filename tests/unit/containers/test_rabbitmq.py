from pytest_celery import RabbitMQContainer


class test_rabbitmq_container:
    def test_client(self, rabbitmq_test_container: RabbitMQContainer):
        assert rabbitmq_test_container.client()
