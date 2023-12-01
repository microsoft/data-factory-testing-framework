from typing import Union

import pytest
from azure_data_factory_testing_framework.exceptions.activity_not_found_error import ActivityNotFoundError
from azure_data_factory_testing_framework.exceptions.dataset_parameter_not_found_error import (
    DatasetParameterNotFoundError,
)
from azure_data_factory_testing_framework.exceptions.expression_parameter_not_found_error import (
    ExpressionParameterNotFoundError,
)
from azure_data_factory_testing_framework.exceptions.linked_service_parameter_not_found_error import (
    LinkedServiceParameterNotFoundError,
)
from azure_data_factory_testing_framework.exceptions.state_iteration_item_not_set_error import (
    StateIterationItemNotSetError,
)
from azure_data_factory_testing_framework.exceptions.variable_not_found_error import VariableNotFoundError
from azure_data_factory_testing_framework.functions.expression_evaluator import ExpressionEvaluator
from azure_data_factory_testing_framework.state.dependency_condition import DependencyCondition
from azure_data_factory_testing_framework.state.pipeline_run_state import PipelineRunState
from azure_data_factory_testing_framework.state.pipeline_run_variable import PipelineRunVariable
from azure_data_factory_testing_framework.state.run_parameter import RunParameter
from azure_data_factory_testing_framework.state.run_parameter_type import RunParameterType
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
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                            Token("EXPRESSION_PARAMETER_NAME", "output"),
                            Token("EXPRESSION_PARAMETER_NAME", "outputName"),
                        ],
                    ),
                    Tree(Token("RULE", "expression_array_indices"), [None]),
                ],
            ),
            id="activity_reference",
        ),
        p(
            "@dataset('datasetName')",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_dataset_reference"),
                        [Token("EXPRESSION_DATASET_NAME", "'datasetName'")],
                    ),
                    Tree(Token("RULE", "expression_array_indices"), [None]),
                ],
            ),
            id="dataset_reference",
        ),
        p(
            "@linkedService('linkedServiceName')",
            Tree(
                Token("RULE", "expression_evaluation"),
                [
                    Tree(
                        Token("RULE", "expression_linked_service_reference"),
                        [Token("EXPRESSION_LINKED_SERVICE_NAME", "'linkedServiceName'")],
                    ),
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                                                    Tree(Token("RULE", "expression_array_indices"), [None]),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                                                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                                                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                                                            Token("EXPRESSION_PARAMETER_NAME", "output"),
                                                            Token("EXPRESSION_PARAMETER_NAME", "abc"),
                                                        ],
                                                    ),
                                                    Tree(Token("RULE", "expression_array_indices"), [None]),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Tree(Token("RULE", "expression_array_indices"), [None]),
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
                                                    Tree(Token("RULE", "expression_array_indices"), [None]),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Tree(
                        Token("RULE", "expression_array_indices"),
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
                            Tree(Token("RULE", "expression_array_indices"), [None]),
                        ],
                    ),
                    Token("LITERAL_LETTER", "/"),
                ],
            ),
            id="string_interpolation",
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
            "@dataset('datasetName')",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Dataset, "datasetName", "datasetNameValue")]),
            "datasetNameValue",
            id="dataset_reference",
        ),
        p(
            "@linkedService('linkedServiceName')",
            PipelineRunState(
                parameters=[RunParameter(RunParameterType.LinkedService, "linkedServiceName", "linkedServiceNameValue")]
            ),
            "linkedServiceNameValue",
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


def test_evaluate_raises_exception_when_pipeline_parameter_not_found() -> None:
    # Arrange
    expression = "@pipeline().parameters.parameter"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(ExpressionParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter 'parameter' not found"


def test_evaluate_raises_exception_when_pipeline_global_parameter_not_found() -> None:
    # Arrange
    expression = "@pipeline().globalParameters.parameter"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(ExpressionParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter 'parameter' not found"


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


def test_evaluate_raises_exception_when_dataset_not_found() -> None:
    # Arrange
    expression = "@dataset('datasetName')"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(DatasetParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Dataset parameter: 'datasetName' not found"


def test_evaluate_raises_exception_when_linked_service_not_found() -> None:
    # Arrange
    expression = "@linkedService('linkedServiceName')"
    evaluator = ExpressionEvaluator()
    state = PipelineRunState()

    # Act
    with pytest.raises(LinkedServiceParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "LinkedService parameter: 'linkedServiceName' not found"


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
    with pytest.raises(ExpressionParameterNotFoundError) as exinfo:
        evaluator.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter 'RunId' not found"
