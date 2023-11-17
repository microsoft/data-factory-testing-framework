import pytest

from azure_data_factory_testing_framework.data_factory.data_factory_test_framework import DataFactoryTestFramework
from azure_data_factory_testing_framework.data_factory.generated.models import (
    DataFactoryElement,
    Expression,
    ExpressionType,
    ForEachActivity,
    SetVariableActivity,
)
from azure_data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable


def test_when_evaluate_child_activities_then_should_return_the_activity_with_item_expression_evaluated() -> None:
    # Arrange
    test_framework = DataFactoryTestFramework()
    for_each_activity = ForEachActivity(
        name="ForEachActivity",
        items=Expression(type=ExpressionType.EXPRESSION, value="@split('a,b,c', ',')"),
        activities=[
            SetVariableActivity(
                name="setVariable",
                variable_name="variable",
                value=DataFactoryElement[str]("item()"),
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
    activities = test_framework.evaluate_activity(for_each_activity, state)

    # Assert
    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"
    assert set_variable_activity.value.value == "a"

    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"
    assert set_variable_activity.value.value == "b"

    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"
    assert set_variable_activity.value.value == "c"

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
