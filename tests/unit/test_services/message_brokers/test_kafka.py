from unittest.mock import patch

from testcontainers.kafka import KafkaContainer

from pytest_celery.test_services.message_brokers.kafka import KafkaBroker


def test_kafka_url(test_session_id, subtests):
    with patch.object(KafkaContainer, "get_exposed_port") as get_exposed_port_mocked:
        get_exposed_port_mocked.return_value = 9093
        container = KafkaContainer()
        service = KafkaBroker(test_session_id, container=container)
        url = "confluentkafka://localhost:9093"

        with subtests.test("RabbitMQ Broker url"):
            assert service.url == url

        with subtests.test("Debug representation includes original url in full"):
            assert repr(service) == f"Kafka Broker <{url}>"
