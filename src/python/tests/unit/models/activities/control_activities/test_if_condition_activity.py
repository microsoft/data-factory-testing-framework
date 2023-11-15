import pytest

from data_factory_testing_framework.generated.models import (
    DataFactoryElement,
    Expression,
    ExpressionType,
    IfConditionActivity,
    SetVariableActivity,
    VariableSpecification,
)
from data_factory_testing_framework.state import PipelineRunState
from data_factory_testing_framework.test_framework import TestFramework

TestFramework()


def test_when_evaluated_should_evaluate_expression() -> None:
    # Arrange
    activity = IfConditionActivity(
        name="IfConditionActivity",
        expression=Expression(type=ExpressionType.EXPRESSION, value="@equals(1, 1)"),
    )

    # Act
    activity.evaluate(PipelineRunState())

    # Assert
    assert activity.expression.evaluated is True


@pytest.mark.parametrize(
    "expression_outcome,expected_activity_name",
    [(True, "setVariableActivity1"), (False, "setVariableActivity2")],
)
def test_when_evaluated_should_evaluate_correct_child_activities(
    expression_outcome: bool,
    expected_activity_name: str,
) -> None:
    # Arrange
    test_framework = TestFramework()
    expression = "@equals(1, 1)" if expression_outcome else "@equals(1, 2)"
    activity = IfConditionActivity(
        name="IfConditionActivity",
        expression=Expression(type=ExpressionType.EXPRESSION, value=expression),
        if_true_activities=[
            SetVariableActivity(
                name="setVariableActivity1",
                variable_name="variable",
                value=DataFactoryElement("dummy"),
            ),
        ],
        if_false_activities=[
            SetVariableActivity(
                name="setVariableActivity2",
                variable_name="variable",
                value=DataFactoryElement("dummy"),
            ),
        ],
    )

    state = PipelineRunState(
        variable_specifications={
            "variable": VariableSpecification(type="String"),
        },
    )

    # Act
    child_activities = list(test_framework.evaluate_activity(activity, state))

    # Assert
    assert len(child_activities) == 1
    assert child_activities[0].name == expected_activity_name
