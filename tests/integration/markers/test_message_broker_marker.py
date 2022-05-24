import pytest


@pytest.mark.parametrize("number_of_brokers", range(1, 2))
@pytest.mark.xfail(reason="work in progress")
def test_successful_with_parameterized_message_brokers(testdir, number_of_brokers):
    testdir.copy_example("test_examples.py")
    result = testdir.runpytest("-k", f"test_successful_when_message_broker_quantity_is_{number_of_brokers}")
    result.assert_outcomes(passed=number_of_brokers)
    assert "warnings" not in result.parseoutcomes()
