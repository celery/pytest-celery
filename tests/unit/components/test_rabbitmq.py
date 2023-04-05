from pytest_celery import RabbitMQTestBroker


class test_rabbitmq_test_broker:
    def test_ready(self, celery_rabbitmq_broker: RabbitMQTestBroker):
        assert celery_rabbitmq_broker.ready()
