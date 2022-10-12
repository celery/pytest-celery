from kafka import KafkaConsumer
from kafka.errors import KafkaError
from rfc3986.builder import URIBuilder
from testcontainers.kafka import KafkaContainer

from pytest_celery.compat import cached_property
from pytest_celery.test_services.message_brokers import MessageBroker


class KafkaBroker(MessageBroker):
    def __init__(self, test_session_id: str, port: int = None, container: KafkaContainer = None):
        container = container or KafkaContainer(port_to_expose=port or 9093)
        super().__init__(container, test_session_id)

    @property
    def url(self):
        host = self._container.get_container_host_ip()
        port = self._container.get_exposed_port(self._container.port_to_expose)

        uri_builder = URIBuilder().add_scheme("confluentkafka")
        if host:
            uri_builder = uri_builder.add_host(host)
        if port:
            uri_builder = uri_builder.add_port(port)

        return uri_builder.geturl()

    def ping(self):
        bootstrap_server = self._container.get_bootstrap_server()
        consumer = KafkaConsumer(group_id="test", bootstrap_servers=[bootstrap_server])
        if not consumer.topics():
            raise KafkaError("Unable to connect with kafka container!")

    @cached_property
    def client(self) -> KafkaConsumer:
        bootstrap_server = self._container.get_bootstrap_server()
        consumer = KafkaConsumer(group_id=self.test_session_id, bootstrap_servers=[bootstrap_server])
        return consumer

    def __repr__(self):
        return f"Kafka Broker <{self.url}>"
