from typing import Union

import pytest
from data_factory_testing_framework.exceptions.activity_not_found_error import ActivityNotFoundError
from data_factory_testing_framework.exceptions.parameter_not_found_error import ParameterNotFoundError
from data_factory_testing_framework.exceptions.state_iteration_item_not_set_error import (
    StateIterationItemNotSetError,
)
from data_factory_testing_framework.exceptions.variable_not_found_error import VariableNotFoundError
from data_factory_testing_framework.functions.expression_evaluator import ExpressionEvaluator
from data_factory_testing_framework.state.dependency_condition import DependencyCondition
from data_factory_testing_framework.state.pipeline_run_state import PipelineRunState
from data_factory_testing_framework.state.pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.state.run_parameter import RunParameter
from data_factory_testing_framework.state.run_parameter_type import RunParameterType
from freezegun import freeze_time
from lark import Token, Tree
from pytest import param as p


@pytest.mark.parametrize(
    ["expression", "expected"],
    [
        p("value", Tree(Token("RULE", "literal_evaluation"), [Token("LITERAL_LETTER", "value")]), id="string_literal"),
        p(
            " value ",
            Tree(Token("RULE", "literal_evaluation"), [Token("LITERAL_LETTER", "value")]),
            id="string_with_ws_literal",
            marks=pytest.mark.skip(""),
        ),
        p("11", Tree(Token("RULE", "literal_evaluation"), [Token("LITERAL_INT", "11")]), id="integer_literal"),
        p(
            "@pipeline().parameters.parameter",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_pipeline_reference"),
                        [
                            Token("EXPRESSION_PIPELINE_PROPERTY", "parameters"),
                            Token("EXPRESSION_PARAMETER_NAME", "parameter"),
                        ],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="pipeline_parameters_reference",
        ),
        p(
            "@pipeline().globalParameters.parameter",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_pipeline_reference"),
                        [
                            Token("EXPRESSION_PIPELINE_PROPERTY", "globalParameters"),
                            Token("EXPRESSION_PARAMETER_NAME", "parameter"),
                        ],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="pipeline_global_parameters_reference",
        ),
        p(
            "@variables('variable')",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_variable_reference"),
                        [Token("EXPRESSION_VARIABLE_NAME", "'variable'")],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="variables_reference",
        ),
        p(
            "@activity('activityName').output.outputName",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_activity_reference"),
                        [
                            Token("EXPRESSION_ACTIVITY_NAME", "'activityName'"),
                            Tree(
                                Token("RULE", "expression_object_accessor"),
                                [Token("EXPRESSION_PARAMETER_NAME", "output")],
                            ),
                        ],
                    ),
                    Tree(
                        Token("RULE", "expression_object_accessor"), [Token("EXPRESSION_PARAMETER_NAME", "outputName")]
                    ),
                ],
            ),
            id="activity_reference",
        ),
        p(
            "@dataset().parameterName",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_dataset_reference"),
                        [Token("EXPRESSION_PARAMETER_NAME", "parameterName")],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="dataset_reference",
        ),
        p(
            "@linkedService().parameterName",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_linked_service_reference"),
                        [Token("EXPRESSION_PARAMETER_NAME", "parameterName")],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="linked_service_reference",
        ),
        p(
            "@item()",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(Token("RULE", "expression_item_reference"), []),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="item_reference",
        ),
        p(
            "@concat('a', 'b' )",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_function_call"),
                        [
                            Token("EXPRESSION_FUNCTION_NAME", "concat"),
                            Tree(
                                Token("RULE", "expression_function_parameters"),
                                [
                                    Tree(Token("RULE", "expression_parameter"), [Token("EXPRESSION_STRING", "'a'")]),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [
                                            Token("EXPRESSION_WS", " "),
                                            Token("EXPRESSION_STRING", "'b'"),
                                            Token("EXPRESSION_WS", " "),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="function_call",
        ),
        p(
            "@concat('a', 'b' )",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_function_call"),
                        [
                            Token("EXPRESSION_FUNCTION_NAME", "concat"),
                            Tree(
                                Token("RULE", "expression_function_parameters"),
                                [
                                    Tree(Token("RULE", "expression_parameter"), [Token("EXPRESSION_STRING", "'a'")]),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [
                                            Token("EXPRESSION_WS", " "),
                                            Token("EXPRESSION_STRING", "'b'"),
                                            Token("EXPRESSION_WS", " "),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="function_call",
        ),
        p(
            "@concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_function_call"),
                        [
                            Token("EXPRESSION_FUNCTION_NAME", "concat"),
                            Tree(
                                Token("RULE", "expression_function_parameters"),
                                [
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [Token("EXPRESSION_STRING", "'https://example.com/jobs/'")],
                                    ),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [Token("EXPRESSION_WS", " "), Token("EXPRESSION_STRING", "'123'''")],
                                    ),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [
                                            Token("EXPRESSION_WS", " "),
                                            Tree(
                                                Token("RULE", "expression_evaluation"),
                                                [
                                                    Tree(
                                                        Token("RULE", "expression_function_call"),
                                                        [
                                                            Token("EXPRESSION_FUNCTION_NAME", "concat"),
                                                            Tree(
                                                                Token("RULE", "expression_function_parameters"),
                                                                [
                                                                    Tree(
                                                                        Token("RULE", "expression_parameter"),
                                                                        [Token("EXPRESSION_STRING", "'&'")],
                                                                    ),
                                                                    Tree(
                                                                        Token("RULE", "expression_parameter"),
                                                                        [
                                                                            Token("EXPRESSION_WS", " "),
                                                                            Token("EXPRESSION_STRING", "'abc,'"),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Tree(Token("RULE", "expression_object_accessor"), []),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="function_call_with_nested_function_and_single_quote",
        ),
        p(
            "concat('https://example.com/jobs/', '123''', variables('abc'), pipeline().parameters.abc, activity('abc').output.abc)",
            Tree(
                Token("RULE", "literal_evaluation"),
                [
                    Token(
                        "LITERAL_LETTER",
                        "concat('https://example.com/jobs/', '123''', variables('abc'), pipeline().parameters.abc, activity('abc').output.abc)",
                    )
                ],
            ),
            id="literal_function_call_with_nested_function_and_single_quote",
        ),
        p(
            "@concat('https://example.com/jobs/', '123''', variables('abc'), pipeline().parameters.abc, activity('abc').output.abc)",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_function_call"),
                        [
                            Token("EXPRESSION_FUNCTION_NAME", "concat"),
                            Tree(
                                Token("RULE", "expression_function_parameters"),
                                [
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [Token("EXPRESSION_STRING", "'https://example.com/jobs/'")],
                                    ),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [Token("EXPRESSION_WS", " "), Token("EXPRESSION_STRING", "'123'''")],
                                    ),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [
                                            Token("EXPRESSION_WS", " "),
                                            Tree(
                                                Token("RULE", "expression_evaluation"),
                                                [
                                                    Tree(
                                                        Token("RULE", "expression_variable_reference"),
                                                        [Token("EXPRESSION_VARIABLE_NAME", "'abc'")],
                                                    ),
                                                    Tree(Token("RULE", "expression_object_accessor"), []),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [
                                            Token("EXPRESSION_WS", " "),
                                            Tree(
                                                Token("RULE", "expression_evaluation"),
                                                [
                                                    Tree(
                                                        Token("RULE", "expression_pipeline_reference"),
                                                        [
                                                            Token("EXPRESSION_PIPELINE_PROPERTY", "parameters"),
                                                            Token("EXPRESSION_PARAMETER_NAME", "abc"),
                                                        ],
                                                    ),
                                                    Tree(Token("RULE", "expression_object_accessor"), []),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [
                                            Token("EXPRESSION_WS", " "),
                                            Tree(
                                                Token("RULE", "expression_evaluation"),
                                                [
                                                    Tree(
                                                        Token("RULE", "expression_activity_reference"),
                                                        [
                                                            Token("EXPRESSION_ACTIVITY_NAME", "'abc'"),
                                                            Tree(
                                                                Token("RULE", "expression_object_accessor"),
                                                                [Token("EXPRESSION_PARAMETER_NAME", "output")],
                                                            ),
                                                        ],
                                                    ),
                                                    Tree(
                                                        Token("RULE", "expression_object_accessor"),
                                                        [Token("EXPRESSION_PARAMETER_NAME", "abc")],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Tree(Token("RULE", "expression_object_accessor"), []),
                ],
            ),
            id="function_call_with_adf_native_functions",
        ),
        p(
            "@createArray('a', createArray('a', 'b'))[1][1]",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_function_call"),
                        [
                            Token("EXPRESSION_FUNCTION_NAME", "createArray"),
                            Tree(
                                Token("RULE", "expression_function_parameters"),
                                [
                                    Tree(Token("RULE", "expression_parameter"), [Token("EXPRESSION_STRING", "'a'")]),
                                    Tree(
                                        Token("RULE", "expression_parameter"),
                                        [
                                            Token("EXPRESSION_WS", " "),
                                            Tree(
                                                Token("RULE", "expression_evaluation"),
                                                [
                                                    Tree(
                                                        Token("RULE", "expression_function_call"),
                                                        [
                                                            Token("EXPRESSION_FUNCTION_NAME", "createArray"),
                                                            Tree(
                                                                Token("RULE", "expression_function_parameters"),
                                                                [
                                                                    Tree(
                                                                        Token("RULE", "expression_parameter"),
                                                                        [Token("EXPRESSION_STRING", "'a'")],
                                                                    ),
                                                                    Tree(
                                                                        Token("RULE", "expression_parameter"),
                                                                        [
                                                                            Token("EXPRESSION_WS", " "),
                                                                            Token("EXPRESSION_STRING", "'b'"),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Tree(Token("RULE", "expression_object_accessor"), []),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Tree(
                        Token("RULE", "expression_object_accessor"),
                        [Token("EXPRESSION_ARRAY_INDEX", "[1]"), Token("EXPRESSION_ARRAY_INDEX", "[1]")],
                    ),
                ],
            ),
            id="function_call_with_nested_array_index",
        ),
        p(
            "/repos/@{pipeline().globalParameters.OpsPrincipalClientId}/",
            Tree(
                Token("RULE", "literal_interpolation"),
                [
                    Token("LITERAL_LETTER", "/repos/"),
                    Tree(
                        Token("RULE", "expression_evaluation"),
                        [
                            Tree(
                                Token("RULE", "expression_pipeline_reference"),
                                [
                                    Token("EXPRESSION_PIPELINE_PROPERTY", "globalParameters"),
                                    Token("EXPRESSION_PARAMETER_NAME", "OpsPrincipalClientId"),
                                ],
                            ),
                            Tree(Token("RULE", "expression_object_accessor"), []),
                        ],
                    ),
                    Token("LITERAL_LETTER", "/"),
                ],
            ),
            id="string_interpolation",
        ),
        p(
            "/repos/@{pipeline().globalParameters.OpsPrincipalClientId}/@{pipeline().parameters.SubPath}",
            Tree(
                Token("RULE", "literal_interpolation"),
                [
                    Token("LITERAL_LETTER", "/repos/"),
                    Tree(
                        Token("RULE", "expression_evaluation"),
                        [
                            Tree(
                                Token("RULE", "expression_pipeline_reference"),
                                [
                                    Token("EXPRESSION_PIPELINE_PROPERTY", "globalParameters"),
                                    Token("EXPRESSION_PARAMETER_NAME", "OpsPrincipalClientId"),
                                ],
                            ),
                            Tree(Token("RULE", "expression_object_accessor"), []),
                        ],
                    ),
                    Token("LITERAL_LETTER", "/"),
                    Tree(
                        Token("RULE", "expression_evaluation"),
                        [
                            Tree(
                                Token("RULE", "expression_pipeline_reference"),
                                [
                                    Token("EXPRESSION_PIPELINE_PROPERTY", "parameters"),
                                    Token("EXPRESSION_PARAMETER_NAME", "SubPath"),
                                ],
                            ),
                            Tree(Token("RULE", "expression_object_accessor"), []),
                        ],
                    ),
                ],
            ),
            id="string_interpolation_multiple_expressions",
        ),
    ],
)
def test_parse(expression: str, expected: Tree[Token]) -> None:
    # Arrange
    evaluator = ExpressionEvaluator()

    # Act
    actual = evaluator.parse(expression)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["expression", "state", "expected"],
    [
        p("value", PipelineRunState(), "value", id="string_literal"),
        p(" value ", PipelineRunState(), " value ", id="string_with_ws_literal"),
        p("11", PipelineRunState(), 11, id="integer_literal"),
        p(
            "@pipeline().parameters.parameter",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Pipeline, "parameter", "value"),
                ]
            ),
            "value",
            id="pipeline_parameters_reference",
        ),
        p(
            "@pipeline().parameters.parameter",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Pipeline, "parameter", 1),
                ]
            ),
            1,
            id="pipeline_parameters_reference",
        ),
        p(
            "@pipeline().globalParameters.parameter",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Global, "parameter", "value"),
                ]
            ),
            "value",
            id="pipeline_global_parameters_reference",
        ),
        p(
            "@variables('variable')",
            PipelineRunState(
                variables=[
                    PipelineRunVariable(name="variable", default_value="value"),
                ]
            ),
            "value",
            id="variables_reference",
        ),
        p(
            "@activity('activityName').output.outputName",
            PipelineRunState(
                pipeline_activity_results={
                    "activityName": {
                        "output": {
                            "outputName": "value",
                        },
                        "status": DependencyCondition.SUCCEEDED,
                    }
                }
            ),
            "value",
            id="activity_reference",
        ),
        p(
            "@dataset().parameterName",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Dataset, "parameterName", "datasetNameValue")]),
            "datasetNameValue",
            id="dataset_reference",
        ),
        p(
            "@linkedService().parameterName",
            PipelineRunState(
                parameters=[RunParameter(RunParameterType.LinkedService, "parameterName", "parameterValue")]
            ),
            "parameterValue",
            id="linked_service_reference",
        ),
        p("@item()", PipelineRunState(iteration_item="value"), "value", id="item_reference"),
        p("@concat('a', 'b' )", PipelineRunState(), "ab", id="function_call"),
        p(
            "concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))",
            PipelineRunState(),
            "concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))",
            id="literal_function_call_with_nested_function_and_single_quote",
        ),
        p(
            "@concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))",
            PipelineRunState(),
            "https://example.com/jobs/123'&abc,",
            id="function_call_with_nested_function_and_single_quote",
        ),
        p(
            "@activity('activityName').output.outputName",
            PipelineRunState(
                pipeline_activity_results={
                    "activityName": {
                        "output": {
                            "outputName": 1,
                        },
                        "status": DependencyCondition.SUCCEEDED,
                    }
                }
            ),
            1,
            id="activity_reference",
        ),
        p(
            "@activity('activityName').output.pipelineReturnValue.test",
            PipelineRunState(
                pipeline_activity_results={
                    "activityName": {
                        "output": {
                            "pipelineReturnValue": {
                                "test": "value",
                            },
                        },
                        "status": DependencyCondition.SUCCEEDED,
                    }
                }
            ),
            "value",
            id="activity_reference_with_nested_property",
        ),
        p("@createArray('a', 'b')", PipelineRunState(), ["a", "b"], id="function_call_array_result"),
        p("@createArray('a', 'b')[1]", PipelineRunState(), "b", id="function_call_with_array_index"),
        p(
            "@createArray('a', createArray('b', 'c'))[1][0]",
            PipelineRunState(),
            "b",
            id="function_call_with_nested_array_index",
        ),
        p(
            "@concat(  'x1'  , \n 'x2','x3'  )",
            PipelineRunState(),
            "x1x2x3",
            id="function_call_with_ws_and_newline",
        ),
        p(
            "@concat(activity('Sample').output.float, 'test')",
            PipelineRunState(
                pipeline_activity_results={
                    "Sample": {
                        "output": {
                            "float": 0.016666666666666666,
                        },
                        "status": DependencyCondition.SUCCEEDED,
                    }
                }
            ),
            "0.016666666666666666test",
            id="function_call_with_nested_property",
            marks=pytest.mark.xfail(
                reason="We do not support automatic type conversion yet. Here float is passed to concat (which expects str)."
            ),
        ),
        p(
            "@activity('Sample').output.billingReference.billableDuration[0].duration",
            PipelineRunState(
                pipeline_activity_results={
                    "Sample": {
                        "output": {
                            "billingReference": {
                                "activityType": "ExternalActivity",
                                "billableDuration": [
                                    {"meterType": "AzureIR", "duration": 0.016666666666666666, "unit": "Hours"}
                                ],
                            }
                        },
                        "status": DependencyCondition.SUCCEEDED,
                    }
                }
            ),
            0.016666666666666666,
            id="activity_reference_with_nested_property_and_array_index",
        ),
        p(
            "@utcNow()",
            PipelineRunState(),
            "2021-11-24T12:11:49.753132Z",
            id="function_call_with_zero_parameters",
        ),
        p(
            "@coalesce(null)",
            PipelineRunState(),
            None,
            id="function_call_with_null_parameter",
        ),
        p(
            "@{pipeline().globalParameters.OpsPrincipalClientId}",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Global, "OpsPrincipalClientId", "dummyId")]),
            "dummyId",
            id="string_interpolation_with_no_surrounding_literals",
        ),
        p(
            "/Repos/@{pipeline().globalParameters.OpsPrincipalClientId}/",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Global, "OpsPrincipalClientId", "dummyId")]),
            "/Repos/dummyId/",
            id="string_interpolation_with_literals",
        ),
        p(
            "/Repos/@{pipeline().globalParameters.OpsPrincipalClientId}/@{pipeline().parameters.SubPath}",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Global, "OpsPrincipalClientId", "dummyId"),
                    RunParameter(RunParameterType.Pipeline, "SubPath", "dummyPath"),
                ]
            ),
            "/Repos/dummyId/dummyPath",
            id="string_interpolation_with_multiple_expressions",
        ),
    ],
)
@freeze_time("2021-11-24 12:11:49.753132")
def test_evaluate(expression: str, state: PipelineRunState, expected: Union[str, int, bool, float]) -> None:
    # Arrange
    evaluator = ExpressionEvaluator()

    # Act
    actual = evaluator.evaluate(expression, state)

    # Assert
    assert actual == expected


def test_evaluate_parameter_with_complex_object_and_array_index() -> None:
    # Arrange
    expression = "@pipeline().parameters.parameter[0].field1.field2"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState(
        parameters=[
            RunParameter(
                RunParameterType.Pipeline,
                "parameter",
                [
                    {
                        "field1": {"field2": "value1"},
                    },
                ],
            ),
        ]
    )

    # Act
    evaluated_value = evaluator.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_raises_exception_when_pipeline_parameter_not_found() -> None:
    # Arrange
    expression = "@pipeline().parameters.parameter"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'parameter' of type 'RunParameterType.Pipeline' not found"


def test_evaluate_raises_exception_when_pipeline_global_parameter_not_found() -> None:
    # Arrange
    expression = "@pipeline().globalParameters.parameter"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'parameter' of type 'RunParameterType.Global' not found"


def test_evaluate_variable_with_complex_object_and_array_index() -> None:
    # Arrange
    expression = "@variables('variable')[0].field1.field2[0]"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(
                name="variable",
                default_value=[
                    {
                        "field1": {"field2": ["value1"]},
                    },
                ],
            ),
        ]
    )

    # Act
    evaluated_value = evaluator.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_raises_exception_when_variable_not_found() -> None:
    # Arrange
    expression = "@variables('variable')"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(VariableNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Variable 'variable' not found"


def test_evaluate_dataset_with_complex_object_and_array_index() -> None:
    # Arrange
    expression = "@dataset().parameterName[0].field1.field2"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState(
        parameters=[
            RunParameter(
                RunParameterType.Dataset,
                "parameterName",
                [
                    {
                        "field1": {"field2": "value1"},
                    },
                ],
            ),
        ]
    )

    # Act
    evaluated_value = evaluator.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_raises_exception_when_dataset_not_found() -> None:
    # Arrange
    expression = "@dataset().parameterName"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'parameterName' of type 'RunParameterType.Dataset' not found"


def test_evaluate_linked_service_with_complex_object_and_array_index() -> None:
    # Arrange
    expression = "@linkedService().parameterName[0].field1.field2"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState(
        parameters=[
            RunParameter(
                RunParameterType.LinkedService,
                "parameterName",
                [
                    {
                        "field1": {"field2": "value1"},
                    },
                ],
            ),
        ]
    )

    # Act
    evaluated_value = evaluator.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_raises_exception_when_linked_service_not_found() -> None:
    # Arrange
    expression = "@linkedService().parameterName"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'parameterName' of type 'RunParameterType.LinkedService' not found"


def test_evaluate_raises_exception_when_activity_not_found() -> None:
    # Arrange
    expression = "@activity('activityName').output.outputName"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(ActivityNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Activity with name 'activityName' not found"


def test_evaluate_raises_exception_when_state_iteration_item_not_set() -> None:
    # Arrange
    expression = "@item()"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(StateIterationItemNotSetError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Iteration item not set."


def test_evaluate_complex_item() -> None:
    # Arrange
    expression = "@item().field1.field2"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState(
        iteration_item={
            "field1": {"field2": "value1"},
        }
    )

    # Act
    evaluated_value = evaluator.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_system_variable() -> None:
    # Arrange
    expression = "@pipeline().RunId"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.System, "RunId", "123"),
        ]
    )

    # Act
    actual = evaluator.evaluate(expression, state)

    # Assert
    assert actual == "123"


def test_evaluate_system_variable_raises_exception_when_parameter_not_set() -> None:
    # Arrange
    expression = "@pipeline().RunId"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'RunId' of type 'RunParameterType.System' not found"


@pytest.mark.parametrize(
    ["json_expression", "accessor", "expected"],
    [
        p(
            '[ "field0", "field1" ]',
            "[1]",
            "field1",
            id="list",
        ),
        p(
            '{ "field0": "value0", "field1": "value1" }',
            ".field1",
            "value1",
            id="field",
        ),
        p(
            '[ { "field0": "value0" }, { "field1": "value1" } ]',
            "[1].field1",
            "value1",
            id="field_in_list",
        ),
        p(
            '[ [ "field0", "value0" ], [ "field1", "value1" ] ]',
            "[1][1]",
            "value1",
            id="list_in_list",
        ),
        p(
            '[ [ { "field0": "value0" }, { "field1": "value1" } ] ]',
            "[0][1].field1",
            "value1",
            id="field_in_nested_list",
        ),
        p(
            '{ "field0": [ "value0", "value1", "value2" ] }',
            ".field0[1]",
            "value1",
            id="list_in_field",
        ),
        p(
            '{ "field0": { "field1": "value1" } }',
            ".field0.field1",
            "value1",
            id="field_in_field",
        ),
        p(
            '{ "field0": { "field1": [ "value1", "value2" ] } }',
            ".field0.field1[1]",
            "value2",
            id="list_in_field_in_field",
        ),
        p(
            '{ "field0": [ { "field1": "value1" }, { "field2": "value2" } ] }',
            ".field0[1].field2",
            "value2",
            id="field_in_list_in_field",
        ),
        p(
            '{ "field0": [ { "field1": [ "value1", "value2" ] } ] }',
            ".field0[0].field1[1]",
            "value2",
            id="list_in_field_in_list_in_field",
        ),
        p(
            '{ "field0": { "field1": [ [ "value0", "value1" ] ] } }',
            ".field0.field1[0][1]",
            "value1",
            id="field_in_field_in_list_in_list",
        ),
        p(
            '[ [ { "field0": "value0" }, { "field1": "value1" } ] ]',
            "[0][1].field1",
            "value1",
            id="list_in_list_in_field_in_field",
        ),
    ],
)
def test_json_nested_object_with_list_and_attributes(json_expression: str, accessor: str, expected: str) -> None:
    expression = f"@json('{json_expression}'){accessor}"

    evaluator = ExpressionEvaluator()
    state = PipelineRunState()
    actual = evaluator.evaluate(expression, state)

    assert actual == expected
