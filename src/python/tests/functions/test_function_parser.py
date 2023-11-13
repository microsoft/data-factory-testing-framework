from data_factory_testing_framework.functions.function_call import FunctionCall
from data_factory_testing_framework.functions.function_parser import parse_expression
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def test_parse_expression_with_nested_function_and_single_quote() -> None:
    # Arrange
    PipelineRunState()
    raw_expression = "concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))"

    # Act
    expression = parse_expression(raw_expression)

    # Assert
    function = expression
    assert isinstance(expression, FunctionCall)
    assert function is not None
    assert function.name == "concat"
    assert len(function.arguments) == 3
    assert function.arguments[0].expression == "'https://example.com/jobs/'"
    assert function.arguments[1].expression == "'123''"

    inner_function = function.arguments[2]
    assert isinstance(inner_function, FunctionCall)
    assert inner_function.name == "concat"
    assert len(inner_function.arguments) == 2
    assert inner_function.arguments[0].expression == "'&'"
    assert inner_function.arguments[1].expression == "'abc,'"


def test_parse_expression_with_adf_native_functions() -> None:
    # Arrange
    PipelineRunState()
    raw_expression = "concat('https://example.com/jobs/', '123''', variables('abc'), pipeline().parameters.abc, activity('abc').output.abc)"

    # Act
    expression = parse_expression(raw_expression)

    # Assert
    function = expression
    assert function.name == "concat"
    assert len(function.arguments) == 5
    assert function.arguments[0].expression == "'https://example.com/jobs/'"
    assert function.arguments[1].expression == "'123''"
    assert function.arguments[2].expression == "variables('abc')"
    assert function.arguments[3].expression == "pipeline().parameters.abc"
    assert function.arguments[4].expression == "activity('abc').output.abc"
