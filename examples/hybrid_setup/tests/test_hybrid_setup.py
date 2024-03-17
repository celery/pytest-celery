from pytest_subtests import SubTests

from pytest_celery import RESULT_TIMEOUT
from pytest_celery import CeleryTestSetup
from pytest_celery import CeleryTestWorker
from pytest_celery import RabbitMQTestBroker
from pytest_celery import ping
from tests.vendors.workers.tasks import job


class TestHybridSetupExample:
    def test_ping(self, celery_setup: CeleryTestSetup):
        assert ping.s().delay().get(timeout=RESULT_TIMEOUT) == "pong"

    def test_job(self, celery_setup: CeleryTestSetup):
        assert job.s().delay().get(timeout=RESULT_TIMEOUT) == "Done!"

    def test_signal(self, celery_setup: CeleryTestSetup):
        celery_setup.worker.assert_log_exists("Worker init handler called!")

    def test_failover(
        self,
        celery_setup: CeleryTestSetup,
        gevent_worker: CeleryTestWorker,
        legacy_worker: CeleryTestWorker,
        session_failover_broker: RabbitMQTestBroker,
        subtests: SubTests,
    ):
        with subtests.test(msg="Kill the main broker"):
            celery_setup.broker.kill()

        with subtests.test(msg="Manually assert the workers"):
            gevent_worker.assert_log_exists("Will retry using next failover.")
            legacy_worker.assert_log_exists("Will retry using next failover.")

        with subtests.test(msg="Use the celery setup to assert the workers"):
            worker: CeleryTestWorker
            for worker in celery_setup.worker_cluster:
                log = f"Connected to amqp://guest:**@{session_failover_broker.hostname()}:5672//"
                worker.assert_log_exists(log)

        with subtests.test(msg="Verify that the workers are still working (publish tasks)"):
            assert job.s().delay().get(timeout=RESULT_TIMEOUT) == "Done!"
