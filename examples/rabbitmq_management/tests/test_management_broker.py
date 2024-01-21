import requests
from requests.auth import HTTPBasicAuth

from pytest_celery import CeleryTestSetup
from tests.conftest import RabbitMQManagementTestBroker


def test_login_to_broker_alone(celery_rabbitmq_broker: RabbitMQManagementTestBroker):
    api = celery_rabbitmq_broker.get_management_url() + "/api/whoami"
    response = requests.get(api, auth=HTTPBasicAuth("guest", "guest"))
    assert response.status_code == 200
    assert response.json()["name"] == "guest"
    assert response.json()["tags"] == ["administrator"]


def test_broker_in_setup(celery_setup: CeleryTestSetup):
    assert isinstance(celery_setup.broker, RabbitMQManagementTestBroker)
    api = celery_setup.broker.get_management_url() + "/api/queues"
    response = requests.get(api, auth=HTTPBasicAuth("guest", "guest"))
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    assert len(list(filter(lambda queues: celery_setup.worker.hostname() in queues["name"], res))) == 1
