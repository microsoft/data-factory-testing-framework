import pytest

from azure_data_factory_testing_framework.data_factory.data_factory_test_framework import DataFactoryTestFramework
from azure_data_factory_testing_framework.data_factory.generated.models import (
    DataFactoryElement,
    Expression,
    ExpressionType,
    SetVariableActivity,
    UntilActivity,
)
from azure_data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable


def test_when_evaluate_until_activity_should_repeat_until_expression_is_true() -> None:
    # Arrange
    test_framework = DataFactoryTestFramework()
    until_activity = UntilActivity(
        name="UntilActivity",
        expression=Expression(type=ExpressionType.EXPRESSION, value="@equals(1, 1)"),
        activities=[
            SetVariableActivity(
                name="setVariable",
                variable_name="variable",
                value=DataFactoryElement[str]("'1'"),
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
    until_activity.expression.evaluate = lambda state: False
    activities = test_framework.evaluate_activity(until_activity, state)

    # Assert
    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"

    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"

    until_activity.expression.evaluate = lambda state: True

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
