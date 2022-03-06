import logging
import os

import pytest


@pytest.mark.parametrize("number_of_brokers", range(1, 2))
# @pytest.mark.xfail(reason="work in progress")
def test_successful_with_parameterized_message_brokers(pytester, number_of_brokers, subtests):
    # pytester.copy_example("marker_examples")
    pytester.makepyfile(
        """
import pytest

from pytest_celery.message_brokers.redis_broker import RedisBroker

@pytest.mark.messagebroker(RedisBroker)
def test_successful_when_message_broker_quantity_is_1(message_broker):
#     # should result in 1 passed test
    pass
"""
    )

    result = pytester.runpytest("test_successful_with_parameterized_message_brokers.py")

    with subtests.test("outcome"):
        result.assert_outcomes(passed=1)

    assert False, str(result.stdout)


# def test_raises_error_when_same_broker_is_specified_twice_without_configuration(testdir):
#     testdir.copy_example("test_examples.py")
#
#     result = testdir.runpytest("-k", "test_raises_error_when_message_broker_is_duplicated_without_configuration")
#
#     result.assert_outcomes(errors=1)
#     assert "warnings" not in result.parseoutcomes()
