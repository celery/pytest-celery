import pytest


@pytest.mark.parametrize("number_of_brokers", range(1, 2))
def test_successful_with_parameterized_message_brokers(testdir, number_of_brokers):
    testdir.copy_example("test_examples.py")
    result = testdir.runpytest("-k", f"test_successful_when_message_broker_quantity_is_{number_of_brokers}")
    result.assert_outcomes(passed=number_of_brokers)
    assert "warnings" not in result.parseoutcomes()


# def test_raises_error_when_same_broker_is_specified_twice_without_configuration(testdir):
#     testdir.copy_example("test_examples.py")
#
#     result = testdir.runpytest("-k", "test_raises_error_when_message_broker_is_duplicated_without_configuration")
#
#     result.assert_outcomes(errors=1)
#     assert "warnings" not in result.parseoutcomes()
