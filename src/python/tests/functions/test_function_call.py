import pytest

from data_factory_testing_framework.exceptions.function_call_invalid_arguments_count_error import (
    FunctionCallInvalidArgumentsCountError,
)
from data_factory_testing_framework.functions.function_parser import parse_expression
from data_factory_testing_framework.generated.models import DependencyCondition, VariableSpecification
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def test_evaluate_expression_with_nested_function():
    # Arrange
    raw_expression = "concat('https://example.com/jobs/,', '123''', concat('&', 'abc,'))"
    expression = parse_expression(raw_expression)

    # Act
    evaluated = expression.evaluate(PipelineRunState())

    # Assert
    assert evaluated == "https://example.com/jobs/,123'&abc,"


def test_evaluate_with_parameter():
    # Arrange
    raw_expression = "concat('https://example.com/jobs/', pipeline().parameters.abc)"
    expression = parse_expression(raw_expression)
    state = PipelineRunState(
        parameters=[
            RunParameter[str](RunParameterType.Pipeline, "abc", "123"),
        ],
    )

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == "https://example.com/jobs/123"


def test_evaluate_with_global_parameter():
    # Arrange
    raw_expression = "concat('https://example.com/jobs/', pipeline().globalParameters.abc)"
    expression = parse_expression(raw_expression)
    state = PipelineRunState(
        parameters=[
            RunParameter[str](RunParameterType.Global, "abc", "123"),
        ],
    )

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == "https://example.com/jobs/123"


def test_evaluate_with_variable():
    # Arrange
    raw_expression = "concat('https://example.com/jobs/', variables('abc'))"
    expression = parse_expression(raw_expression)
    state = PipelineRunState(
        variable_specifications={
            "abc": VariableSpecification(type="String", default_value="123"),
        },
    )

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == "https://example.com/jobs/123"


def test_evaluate_with_activity_output():
    # Arrange
    raw_expression = "concat('https://example.com/jobs/', activity('abc').output.abc)"
    expression = parse_expression(raw_expression)
    state = PipelineRunState()
    state.add_activity_result("abc", DependencyCondition.SUCCEEDED, {"abc": "123"})

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == "https://example.com/jobs/123"


def test_evaluate_with_activity_output_and_variable():
    # Arrange
    raw_expression = "concat('https://example.com/jobs/', activity('abc').output.abc, '/', variables('abc'))"
    expression = parse_expression(raw_expression)
    state = PipelineRunState(
        variable_specifications={
            "abc": VariableSpecification(type="String", default_value="456"),
        },
    )
    state.add_activity_result("abc", DependencyCondition.SUCCEEDED, {"abc": "123"})

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == "https://example.com/jobs/123/456"


def test_evaluate_with_activity_output_and_variable_and_parameters():
    # Arrange
    raw_expression = (
        "concat('https://example.com/jobs/', activity('abc').output.abc, '/', "
        "variables('abc'), '/', pipeline().parameters.abc, '/', pipeline().globalParameters.abc)"
    )
    expression = parse_expression(raw_expression)
    state = PipelineRunState(
        variable_specifications={
            "abc": VariableSpecification(type="String", default_value="456"),
        },
        parameters=[
            RunParameter(RunParameterType.Pipeline, "abc", "789"),
            RunParameter(RunParameterType.Global, "abc", "10"),
        ],
    )
    state.add_activity_result("abc", DependencyCondition.SUCCEEDED, {"abc": "123"})

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == "https://example.com/jobs/123/456/789/10"


@pytest.mark.parametrize(
    "left, right, expected",
    [
        ("'abc'", "'abc'", True),
        ("'abc'", "'abc1'", False),
        ("1", "1", True),
        ("1", "2", False),
    ],
)
def test_evaluate_equals_expression(left, right, expected):
    # Arrange
    raw_expression = f"equals({left}, {right})"
    expression = parse_expression(raw_expression)

    # Act
    evaluated = expression.evaluate(PipelineRunState())

    # Assert
    assert evaluated == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (1, 1, True),
        (1, 2, False),
        (2, 2, True),
        (0, -1, False),
    ],
)
def test_evaluate_equals_int_expression(left, right, expected):
    # Arrange
    raw_expression = f"equals({left}, {right})"
    expression = parse_expression(raw_expression)

    # Act
    evaluated = expression.evaluate(PipelineRunState())

    # Assert
    assert evaluated == expected


@pytest.mark.parametrize(
    "key, expected",
    [
        ("SomeKey", True),
        ("SomeKey2", True),
        ("SomeKey3", False),
    ],
)
def test_contains_dictionary_key_expression(key, expected):
    # Arrange
    state = PipelineRunState()
    state.add_activity_result(
        "someActivityOutputingDictionary",
        DependencyCondition.SUCCEEDED,
        {"SomeDictionary": {"SomeKey": "SomeValue", "SomeKey2": "SomeValue2"}},
    )
    raw_expression = f"@contains(activity('someActivityOutputingDictionary').output.SomeDictionary, '{key}')"
    expression = parse_expression(raw_expression)

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == expected


@pytest.mark.parametrize(
    "key, expected",
    [
        ("SomeItem", True),
        ("SomeItem2", True),
        ("SomeItem3", False),
    ],
)
def test_contains_list_item_expression(key, expected):
    # Arrange
    state = PipelineRunState()
    state.add_activity_result(
        "someActivityOutputingList",
        DependencyCondition.SUCCEEDED,
        {"SomeList": ["SomeItem", "SomeItem2"]},
    )
    raw_expression = f"@contains(activity('someActivityOutputingList').output.SomeList, '{key}')"
    expression = parse_expression(raw_expression)

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == expected


@pytest.mark.parametrize(
    "substring, expected",
    [
        ("PartOfString", True),
        ("NotPartOfString", False),
    ],
)
def test_contains_string_expression(substring, expected):
    # Arrange
    state = PipelineRunState()
    state.add_activity_result(
        "someActivityOutputingString",
        DependencyCondition.SUCCEEDED,
        {"SomeString": "A message that contains PartOfString!"},
    )
    raw_expression = f"@contains(activity('someActivityOutputingString').output.SomeString, '{substring}')"
    expression = parse_expression(raw_expression)

    # Act
    evaluated = expression.evaluate(state)

    # Assert
    assert evaluated == expected


def test_function_call_wrong_arguments_error():
    # Arrange
    raw_expression = "trim('abc', 'a', 'b')"
    expression = parse_expression(raw_expression)

    # Act
    with pytest.raises(FunctionCallInvalidArgumentsCountError) as exception_info:
        expression.evaluate(PipelineRunState())

    # Assert
    assert (
        exception_info.value.args[0]
        == 'FunctionCall trim has invalid arguments count. Evaluated arguments: "abc, a, b". Expected argument types: text, trim_argument'
    )
