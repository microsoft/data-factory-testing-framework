from unittest.mock import Mock

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.models import DataFactoryElement, DataFactoryObjectType
from data_factory_testing_framework.models.activities import SetVariableActivity, UntilActivity
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable, RunParameter, RunParameterType


def test_when_evaluate_until_activity_should_repeat_until_expression_is_true(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric)
    until_activity = UntilActivity(
        name="UntilActivity",
        typeProperties={
            "expression": DataFactoryElement("@equals(1, 1)"),
        },
        activities=[
            SetVariableActivity(
                name="setVariable",
                typeProperties={
                    "variableName": "variable",
                    "value": DataFactoryElement("'1'"),
                },
                depends_on=[],
            ),
        ],
        depends_on=[],
    )

    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="variable", default_value=""),
        ],
    )

    # Act
    monkeypatch.setattr(until_activity.expression, "evaluate", lambda state: False)
    activities = test_framework.evaluate_activity(until_activity, state)

    # Assert
    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"

    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"

    monkeypatch.setattr(until_activity.expression, "evaluate", lambda state: True)

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)


def test_evaluate_pipeline_should_pass_iteration_item_to_child_activities() -> None:
    # Arrange
    state = PipelineRunState(variables=[PipelineRunVariable("variable", None)], iteration_item="some-item")
    until_activity = UntilActivity(
        name="UntilActivity",
        typeProperties={
            "expression": DataFactoryElement("@equals(1,1)"),
        },
        activities=[],
    )
    evaluator = Mock(return_value=[])

    # Act
    list(until_activity.evaluate_control_activities(state, evaluator))

    # Assert
    assert evaluator.call_args[0][1].iteration_item == "some-item"


@pytest.mark.parametrize(("evaluated_value"), [1, 1.1, "string-value", {}, [], None])
def test_evaluated_raises_error_when_evaluated_value_is_not_a_bool(evaluated_value: DataFactoryObjectType) -> None:
    # Arrange
    state = PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "input_values", evaluated_value)])
    activity = UntilActivity(
        name="UntilActivity",
        typeProperties={
            "expression": DataFactoryElement("@pipeline().parameters.input_values"),
        },
        activities=[],
    )
    evaluator = Mock(return_value=[])

    # Act
    with pytest.raises(ControlActivityExpressionEvaluatedNotToExpectedTypeError) as ex_info:
        list(activity.evaluate_control_activities(state, evaluator))

    assert (
        ex_info.value.args[0]
        == "Iteration expression of Activity: 'UntilActivity' does not evaluate to the expected type: 'bool'."
    )
