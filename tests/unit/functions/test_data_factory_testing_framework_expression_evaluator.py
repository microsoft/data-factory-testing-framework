from typing import Union

import pytest
from data_factory_testing_framework._expression_runtime.data_factory_expression import (
    ExpressionTransformer as DataFactoryExpressionTransformer,
)
from data_factory_testing_framework._expression_runtime.expression_runtime import ExpressionRuntime
from data_factory_testing_framework._pythonnet.data_factory_testing_framework_expressions_evaluator import (
    DataFactoryTestingFrameworkExpressionsEvaluator,
)
from data_factory_testing_framework.exceptions import (
    ActivityNotFoundError,
    ParameterNotFoundError,
    StateIterationItemNotSetError,
    VariableNotFoundError,
)
from data_factory_testing_framework.state import (
    ActivityResult,
    DependencyCondition,
    PipelineRunState,
    PipelineRunVariable,
    RunParameter,
    RunParameterType,
)
from pytest import param as p


@pytest.mark.parametrize(
    ["expression", "state", "expected_expressions_evaluator_expression", "expected_evaluation"],
    [
        p("value", PipelineRunState(), "value", "value", id="string_literal"),
        p(" value ", PipelineRunState(), " value ", " value ", id="string_with_ws_literal"),
        p("11", PipelineRunState(), "11", "11", id="integer_literal"),
        p(
            "@pipeline().parameters.parameter",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Pipeline, "parameter", "value"),
                ]
            ),
            "@pipeline().parameters.parameter",
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
            "@pipeline().parameters.parameter",
            1,
            id="pipeline_parameters_reference",
        ),
        p(
            "@pipeline().parameters.parameter",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Pipeline, "parameter", {"field1": "value1"}),
                ]
            ),
            "@pipeline().parameters.parameter",
            {"field1": "value1"},
            id="pipeline_parameters_reference_complex",
        ),
        p(
            "@pipeline().globalParameters.parameter",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Global, "parameter", "value"),
                ]
            ),
            "@pipeline().globalParameters.parameter",
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
            "@variables('variable')",
            "value",
            id="variables_reference",
        ),
        p(
            "@activity('activityName').output.outputName",
            PipelineRunState(
                activity_results=[
                    ActivityResult(
                        activity_name="activityName",
                        status=DependencyCondition.SUCCEEDED,
                        output={
                            "outputName": "value",
                        },
                    ),
                ]
            ),
            "@activity('activityName').output.outputName",
            "value",
            id="activity_reference",
        ),
        p(
            "@dataset().parameterName",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Dataset, "parameterName", "datasetNameValue")]),
            "@pipeline().dataset.parameterName",
            "datasetNameValue",
            id="dataset_reference",
        ),
        p(
            "@linkedService().parameterName",
            PipelineRunState(
                parameters=[RunParameter(RunParameterType.LinkedService, "parameterName", "parameterValue")]
            ),
            "@pipeline().linkedService.parameterName",
            "parameterValue",
            id="linked_service_reference",
        ),
        p("@item()", PipelineRunState(iteration_item="value"), "@item()", "value", id="item_reference"),
        p("@item() ", PipelineRunState(iteration_item="value"), "@item() ", "value", id="item_reference_with_ws"),
        p("@concat('a', 'b' )", PipelineRunState(), "@concat('a', 'b' )", "ab", id="function_call"),
        p(
            "@concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))",
            PipelineRunState(),
            "@concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))",
            "https://example.com/jobs/123'&abc,",
            id="literal_function_call_with_nested_function_and_single_quote",
        ),
        p(
            "@concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))",
            PipelineRunState(),
            "@concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))",
            "https://example.com/jobs/123'&abc,",
            id="function_call_with_nested_function_and_single_quote",
        ),
        p(
            "@activity('activityName').output.outputName",
            PipelineRunState(
                activity_results=[
                    ActivityResult(
                        activity_name="activityName",
                        status=DependencyCondition.SUCCEEDED,
                        output={
                            "outputName": 1,
                        },
                    ),
                ]
            ),
            "@activity('activityName').output.outputName",
            1,
            id="activity_reference",
        ),
        p(
            "@activity('activityName').output.pipelineReturnValue.test",
            PipelineRunState(
                activity_results=[
                    ActivityResult(
                        activity_name="activityName",
                        status=DependencyCondition.SUCCEEDED,
                        output={
                            "pipelineReturnValue": {
                                "test": "value",
                            },
                        },
                    ),
                ]
            ),
            "@activity('activityName').output.pipelineReturnValue.test",
            "value",
            id="activity_reference_with_nested_property",
        ),
        p(
            "@createArray('a', 'b')",
            PipelineRunState(),
            "@createArray('a', 'b')",
            ["a", "b"],
            id="function_call_array_result",
        ),
        p(
            "@createArray('a', 'b')[1]",
            PipelineRunState(),
            "@createArray('a', 'b')[1]",
            "b",
            id="function_call_with_array_index",
        ),
        p(
            "@createArray('a', createArray('b', 'c'))[1][0]",
            PipelineRunState(),
            "@createArray('a', createArray('b', 'c'))[1][0]",
            "b",
            id="function_call_with_nested_array_index",
        ),
        p(
            "@concat(  'x1'  , \n 'x2','x3'  )",
            PipelineRunState(),
            "@concat(  'x1'  , \n 'x2','x3'  )",
            "x1x2x3",
            id="function_call_with_ws_and_newline",
        ),
        p(
            "@concat(activity('Sample').output.float, 'test')",
            PipelineRunState(
                activity_results=[
                    ActivityResult(
                        activity_name="Sample",
                        status=DependencyCondition.SUCCEEDED,
                        output={
                            "float": 0.016666666666666666,
                        },
                    ),
                ]
            ),
            "@concat(activity('Sample').output.float, 'test')",
            "0.016666666666666666test",
            id="function_call_with_nested_property",
        ),
        p(
            "@concat('https://example.com/jobs/', '123''', variables('abc'), pipeline().parameters.abc, activity('abc').output.abc)",
            PipelineRunState(
                variables=[PipelineRunVariable("abc", "defaultvalue_")],
                parameters=[RunParameter(RunParameterType.Pipeline, "abc", "testvalue_02")],
                activity_results=[
                    ActivityResult(
                        activity_name="abc",
                        status=DependencyCondition.SUCCEEDED,
                        output={
                            "abc": "_testvalue_01",
                        },
                    )
                ],
            ),
            "@concat('https://example.com/jobs/', '123''', variables('abc'), pipeline().parameters.abc, activity('abc').output.abc)",
            "https://example.com/jobs/123'defaultvalue_testvalue_02_testvalue_01",
            id="function_call_with_nested_references",
        ),
        p(
            "@createArray('a', createArray('a', 'b'))[1][1]",
            PipelineRunState(),
            "@createArray('a', createArray('a', 'b'))[1][1]",
            "b",
            id="function_call_with_nested_array_index",
        ),
        p(
            "/repos/@{pipeline().globalParameters.OpsPrincipalClientId}/",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Global, "OpsPrincipalClientId", "id")]),
            "/repos/@{pipeline().globalParameters.OpsPrincipalClientId}/",
            "/repos/id/",
            id="string_interpolation",
        ),
        p(
            "/repos/@{pipeline().globalParameters.OpsPrincipalClientId}/@{pipeline().parameters.SubPath}",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Global, "OpsPrincipalClientId", "id"),
                    RunParameter(RunParameterType.Pipeline, "SubPath", "apath"),
                ]
            ),
            "/repos/@{pipeline().globalParameters.OpsPrincipalClientId}/@{pipeline().parameters.SubPath}",
            "/repos/id/apath",
            id="string_interpolation_with_multiple_interpolations",
        ),
        p(
            "@activity('Sample').output.billingReference.billableDuration[0].duration",
            PipelineRunState(
                activity_results=[
                    ActivityResult(
                        activity_name="Sample",
                        status=DependencyCondition.SUCCEEDED,
                        output={
                            "billingReference": {
                                "activityType": "ExternalActivity",
                                "billableDuration": [
                                    {"meterType": "AzureIR", "duration": 0.016666666666666666, "unit": "Hours"}
                                ],
                            }
                        },
                    ),
                ]
            ),
            "@activity('Sample').output.billingReference.billableDuration[0].duration",
            0.016666666666666666,
            id="activity_reference_with_nested_property_and_array_index",
        ),
        p(
            "@coalesce(null)",
            PipelineRunState(),
            "@coalesce(null)",
            None,
            id="function_call_with_null_parameter",
        ),
        p(
            "@{pipeline().globalParameters.OpsPrincipalClientId}",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Global, "OpsPrincipalClientId", "dummyId")]),
            "@{pipeline().globalParameters.OpsPrincipalClientId}",
            "dummyId",
            id="string_interpolation_with_no_surrounding_literals",
        ),
        p(
            "/Repos/@{pipeline().globalParameters.OpsPrincipalClientId}/",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Global, "OpsPrincipalClientId", "dummyId")]),
            "/Repos/@{pipeline().globalParameters.OpsPrincipalClientId}/",
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
            "/Repos/@{pipeline().globalParameters.OpsPrincipalClientId}/@{pipeline().parameters.SubPath}",
            "/Repos/dummyId/dummyPath",
            id="string_interpolation_with_multiple_expressions",
        ),
        p(
            "@concat(variables('variable_test'), pipeline().parameters.parameter_test)",
            PipelineRunState(
                variables=[PipelineRunVariable("variable_test", "variable_test_value")],
                parameters=[RunParameter(RunParameterType.Pipeline, "parameter_test", "parameter_test_value")],
            ),
            "@concat(variables('variable_test'), pipeline().parameters.parameter_test)",
            "variable_test_valueparameter_test_value",
            id="variable_and_parameter_reference",
        ),
        p(
            "@activity('get nested object').output.pipelineReturnValue.returnValue.attribute1[pipeline().parameters.parameter]",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Pipeline, "parameter", "param1"),
                ],
                activity_results=[
                    ActivityResult(
                        activity_name="get nested object",
                        status=DependencyCondition.SUCCEEDED,
                        output={
                            "pipelineReturnValue": {
                                "returnValue": {
                                    "attribute1": {
                                            "param1": "value1",
                                        },
                                }
                            }
                        },
                    )
                ]
            ),
            "@activity('get nested object').output.pipelineReturnValue.returnValue.attribute1[pipeline().parameters.parameter]",
            "value1",
            id="activity_reference_with_nested_property_and_string_array_index",
        )
    ],
)
def test_evaluate(
    expression: str,
    state: PipelineRunState,
    expected_expressions_evaluator_expression: str,
    expected_evaluation: Union[str, int, bool, float],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    data_factory_expression_transformer = DataFactoryExpressionTransformer()

    # Act populating the expression
    dftf_evaluator_expression = data_factory_expression_transformer.transform_to_dftf_evaluator_expression(
        expression, state
    )

    # Assert population
    assert dftf_evaluator_expression == expected_expressions_evaluator_expression

    # Act evaluating the expression
    dftf_evaluator = DataFactoryTestingFrameworkExpressionsEvaluator()
    actual = dftf_evaluator.evaluate(dftf_evaluator_expression, state)

    # Assert evaluation
    assert actual == expected_evaluation


def test_evaluate_function_names_are_case_insensitive() -> None:
    # Arrange
    expression = "@CONCAT('a', 'b')"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value == "ab"


def test_evaluate_function_with_null_conditional_operator() -> None:
    # Arrange
    expression = "@pipeline().parameters.parameter.field1?.field2"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState(
        parameters=[
            RunParameter(
                RunParameterType.Pipeline,
                "parameter",
                {
                    "field1": {"field2": "value1"},
                },
            ),
        ]
    )

    # Act
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_function_with_null_conditional_operator_and_null_value() -> None:
    # Arrange
    expression = "@pipeline().parameters.parameter?.field1?.field2"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState(
        parameters=[
            RunParameter(
                RunParameterType.Pipeline,
                "parameter",
                {
                    "field1": None,
                },
            ),
        ]
    )

    # Act
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value is None


def test_evaluate_function_with_null_conditional_operator_and_system_variable() -> None:
    # Arrange
    expression = "@pipeline()?.TriggeredByPipelineRunId"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value is None


def test_evaluate_parameter_with_complex_object_and_array_index() -> None:
    # Arrange
    expression = "@pipeline().parameters.parameter[0].field1.field2"
    expression_runtime = ExpressionRuntime()
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
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_raises_exception_when_pipeline_parameter_not_found() -> None:
    # Arrange
    expression = "@pipeline().parameters.parameter"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'parameter' of type 'RunParameterType.Pipeline' not found"


def test_evaluate_raises_exception_when_pipeline_global_parameter_not_found() -> None:
    # Arrange
    expression = "@pipeline().globalParameters.parameter"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'parameter' of type 'RunParameterType.Global' not found"


def test_evaluate_variable_with_complex_object_and_array_index() -> None:
    # Arrange
    expression = "@variables('variable')[0].field1.field2[0]"
    expression_runtime = ExpressionRuntime()
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
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_raises_exception_when_variable_not_found() -> None:
    # Arrange
    expression = "@variables('variable')"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    with pytest.raises(VariableNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Variable 'variable' not found"


def test_evaluate_dataset_with_complex_object_and_array_index() -> None:
    # Arrange
    expression = "@dataset().parameterName[0].field1.field2"
    expression_runtime = ExpressionRuntime()
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
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_raises_exception_when_dataset_not_found() -> None:
    # Arrange
    expression = "@dataset().parameterName"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'parameterName' of type 'RunParameterType.Dataset' not found"


def test_evaluate_linked_service_with_complex_object_and_array_index() -> None:
    # Arrange
    expression = "@linkedService().parameterName[0].field1.field2"
    expression_runtime = ExpressionRuntime()
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
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_raises_exception_when_linked_service_not_found() -> None:
    # Arrange
    expression = "@linkedService().parameterName"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Parameter: 'parameterName' of type 'RunParameterType.LinkedService' not found"


def test_evaluate_raises_exception_when_activity_not_found() -> None:
    # Arrange
    expression = "@activity('activityName').output.outputName"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    with pytest.raises(ActivityNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Activity with name 'activityName' not found"


def test_evaluate_raises_exception_when_state_iteration_item_not_set() -> None:
    # Arrange
    expression = "@item()"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    with pytest.raises(StateIterationItemNotSetError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == "Iteration item not set."


def test_evaluate_complex_item() -> None:
    # Arrange
    expression = "@item().field1.field2"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState(
        iteration_item={
            "field1": {"field2": "value1"},
        }
    )

    # Act
    evaluated_value = expression_runtime.evaluate(expression, state)

    # Assert
    assert evaluated_value == "value1"


def test_evaluate_system_variable() -> None:
    # Arrange
    expression = "@pipeline().RunId"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.System, "RunId", "123"),
        ]
    )

    # Act
    actual = expression_runtime.evaluate(expression, state)

    # Assert
    assert actual == "123"


def test_evaluate_system_variable_raises_exception_when_parameter_not_set() -> None:
    # Arrange
    expression = "@pipeline().RunId"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

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

    expression_runtime = ExpressionRuntime()
    state = PipelineRunState()
    actual = expression_runtime.evaluate(expression, state)

    assert actual == expected


@pytest.mark.parametrize(
    ["logical_operator", "parameter_left", "parameter_right", "state", "expected"],
    [
        p(
            "or",
            "aval",
            "bval",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "a", "aval")]),
            True,
            id="or_true_with_left_parameter_short_circuit",
        ),
        p(
            "or",
            "OTHER",
            "bval",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "a", "aval")]),
            ParameterNotFoundError,
            id="or_false_with_right_parameter_exception",
        ),
        p(
            "or",
            "OTHER",
            "bval",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Pipeline, "a", "aval"),
                    RunParameter(RunParameterType.Pipeline, "b", "bval"),
                ]
            ),
            True,
            id="or_true_with_right_parameter",
        ),
        p(
            "or",
            "OTHER",
            "OTHER",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "a", "aval")]),
            ParameterNotFoundError,
            id="or_false_with_both_parameters_right_exception",
        ),
        p(
            "or",
            "OTHER",
            "OTHER",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Pipeline, "a", "aval"),
                    RunParameter(RunParameterType.Pipeline, "b", "bval"),
                ]
            ),
            False,
            id="or_false_with_both_parameters",
        ),
        p(
            "and",
            "aval",
            "bval",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "a", "aval")]),
            ParameterNotFoundError,
            id="and_false_with_right_parameter_exception",
        ),
        p(
            "and",
            "OTHER",
            "bval",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "a", "aval")]),
            False,
            id="and_false_with_left_parameter_short_circuit",
        ),
        p(
            "and",
            "OTHER",
            "bval",
            PipelineRunState(
                parameters=[
                    RunParameter(RunParameterType.Pipeline, "a", "aval"),
                    RunParameter(RunParameterType.Pipeline, "b", "bval"),
                ]
            ),
            False,
            id="and_false_with_right_parameter",
        ),
    ],
)
def test_boolean_operators_short_circuit(
    logical_operator: str,
    parameter_left: str,
    parameter_right: str,
    state: PipelineRunState,
    expected: Union[bool, Exception],
) -> None:
    # Arrange
    expression = f"@{logical_operator}(equals(pipeline().parameters.a,'{parameter_left}'),equals(pipeline().parameters.b,'{parameter_right}'))"

    expression_runtime = ExpressionRuntime()

    # Act / Assert
    if isinstance(expected, bool):
        actual = expression_runtime.evaluate(expression, state)
        assert actual == expected
    else:
        with pytest.raises(expected):
            expression_runtime.evaluate(expression, state)


@pytest.mark.parametrize(
    ["expression", "state", "expected"],
    [
        p(
            "@if(equals(pipeline().parameters.a, 'MATCH'), 'LEFT_BRANCH', 'RIGHT_BRANCH')",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "a", "MATCH")]),
            "LEFT_BRANCH",
            id="if_true",
        ),
        p(
            "@if(equals(pipeline().parameters.a, 'NO_MATCH'), 'LEFT_BRANCH', 'RIGHT_BRANCH')",
            PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "a", "MATCH")]),
            "RIGHT_BRANCH",
            id="if_false",
        ),
        p(
            "@if(equals('MATCH', 'MATCH'), pipeline().parameters.b, 'RIGHT_BRANCH')",
            PipelineRunState(),
            ParameterNotFoundError,
            id="if_false_left_no_parameter",
        ),
        p(
            "@if(equals('MATCH', 'MATCH'), 'LEFT_BRANCH', pipeline().parameters.b)",
            PipelineRunState(),
            "LEFT_BRANCH",
            id="if_true_right_no_parameter",
        ),
    ],
)
def test_conditional_expression_with_branching(
    expression: str, state: PipelineRunState, expected: Union[str, int, bool, float, Exception]
) -> None:
    # Arrange
    expression_runtime = ExpressionRuntime()

    # Act / Assert
    if isinstance(expected, (str, int, bool, float)):
        actual = expression_runtime.evaluate(expression, state)

        # Assert
        assert actual == expected
    else:
        with pytest.raises(expected):
            expression_runtime.evaluate(expression, state)


@pytest.mark.parametrize(
    "run_parameter_type, parameter_prefix",
    [
        (RunParameterType.Pipeline, "pipeline().parameters"),
        (RunParameterType.Global, "pipeline().globalParameters"),
        (RunParameterType.Dataset, "pipeline().dataset"),
        (RunParameterType.LinkedService, "pipeline().linkedService"),
        (RunParameterType.System, "pipeline()"),
    ],
)
def test_complex_expression_with_missing_parameter(run_parameter_type: RunParameterType, parameter_prefix: str) -> None:
    # Arrange
    expression = f"@concat(pipeline().parameters.parameter, {parameter_prefix}.parameter2)"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "parameter", "value")])

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == f"Parameter: 'parameter2' of type '{run_parameter_type}' not found"


@pytest.mark.parametrize(
    "run_parameter_type, parameter_prefix",
    [
        (RunParameterType.Global, "pipeline().globalParameters"),
        (RunParameterType.Dataset, "pipeline().dataset"),
        (RunParameterType.LinkedService, "pipeline().linkedService"),
        (RunParameterType.System, "pipeline()"),
    ],
)
def test_complex_expression_with_missing_parameter_with_same_name_of_another_type(
    run_parameter_type: RunParameterType, parameter_prefix: str
) -> None:
    # Arrange
    expression = f"@concat(pipeline().parameters.parameter, {parameter_prefix}.parameter)"
    expression_runtime = ExpressionRuntime()
    state = PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "parameter", "value")])

    # Act
    with pytest.raises(ParameterNotFoundError) as exinfo:
        expression_runtime.evaluate(expression, state)

    # Assert
    assert str(exinfo.value) == f"Parameter: 'parameter' of type '{run_parameter_type}' not found"
