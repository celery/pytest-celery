import pytest


@pytest.mark.parametrize("number_of_brokers", (1,))
def test_successful_with_parameterized_message_brokers(pytester, number_of_brokers, subtests):
    pytester.copy_example("markers")

    result = pytester.runpytest("-k", f"test_successful_when_message_broker_quantity_is_{number_of_brokers}")

    with subtests.test("outcome"):
        result.assert_outcomes(passed=1)


def test_successful_simple_task(pytester, subtests):
    pytester.copy_example("markers")

    result = pytester.runpytest("-k", f"test_simple_task")

    with subtests.test("outcome"):
        result.assert_outcomes(passed=1)