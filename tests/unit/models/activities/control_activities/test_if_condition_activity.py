from unittest.mock import Mock

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.models import DataFactoryElement, DataFactoryObjectType
from data_factory_testing_framework.models.activities import IfConditionActivity, SetVariableActivity
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable, RunParameter, RunParameterType


def test_when_evaluated_should_evaluate_expression() -> None:
    # Arrange
    activity = IfConditionActivity(
        name="IfConditionActivity",
        if_true_activities=[],
        if_false_activities=[],
        typeProperties={"expression": DataFactoryElement("@equals(1, 1)")},
    )

    # Act
    activity.evaluate(PipelineRunState())

    # Assert
    assert activity.expression.result


@pytest.mark.parametrize(
    "expression_outcome,expected_activity_name",
    [(True, "setVariableActivity1"), (False, "setVariableActivity2")],
)
def test_when_evaluated_should_evaluate_correct_child_activities(
    expression_outcome: bool,
    expected_activity_name: str,
) -> None:
    # Arrange
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric)
    expression = "@equals(1, 1)" if expression_outcome else "@equals(1, 2)"
    activity = IfConditionActivity(
        name="IfConditionActivity",
        typeProperties={
            "expression": DataFactoryElement(expression),
        },
        if_true_activities=[
            SetVariableActivity(
                name="setVariableActivity1",
                typeProperties={
                    "variableName": "variable",
                    "value": DataFactoryElement("dummy"),
                },
            ),
        ],
        if_false_activities=[
            SetVariableActivity(
                name="setVariableActivity2",
                typeProperties={
                    "variableName": "variable",
                    "value": DataFactoryElement("dummy"),
                },
            ),
        ],
    )

    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="variable", default_value=""),
        ],
    )

    # Act
    child_activities = list(test_framework.evaluate_activity(activity, state))

    # Assert
    assert len(child_activities) == 1
    assert child_activities[0].name == expected_activity_name


def test_evaluate_pipeline_should_pass_iteration_item_to_child_activities() -> None:
    # Arrange
    state = PipelineRunState(variables=[PipelineRunVariable("variable", None)], iteration_item="some-item")
    activity = IfConditionActivity(
        name="IfCondition",
        if_true_activities=[],
        if_false_activities=[],
        typeProperties={
            "expression": DataFactoryElement("some-expression"),
        },
    )
    evaluator = Mock(return_value=[])

    # Act
    list(activity.evaluate_control_activities(state, evaluator))

    # Assert
    assert evaluator.call_args[0][1].iteration_item == "some-item"


@pytest.mark.parametrize(("evaluated_value"), [1, 1.1, "string-value", {}, [], None])
def test_evaluated_raises_error_when_evaluated_value_is_not_a_bool(evaluated_value: DataFactoryObjectType) -> None:
    # Arrange
    state = PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "input_values", evaluated_value)])
    activity = IfConditionActivity(
        name="IfCondition",
        if_true_activities=[],
        if_false_activities=[],
        typeProperties={
            "expression": DataFactoryElement("@pipeline().parameters.input_values"),
        },
    )

    # Act
    with pytest.raises(ControlActivityExpressionEvaluatedNotToExpectedTypeError) as ex_info:
        activity.evaluate(state)

    assert (
        ex_info.value.args[0]
        == "Iteration expression of Activity: 'IfCondition' does not evaluate to the expected type: 'bool'."
    )
