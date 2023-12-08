import pytest
from data_factory_testing_framework.models.activities.if_condition_activity import IfConditionActivity
from data_factory_testing_framework.models.activities.set_variable_activity import SetVariableActivity
from data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable
from data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


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
    assert activity.expression.value


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
