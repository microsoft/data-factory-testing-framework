import pytest
from data_factory_testing_framework import TestFramework
from data_factory_testing_framework.models import DataFactoryElement
from data_factory_testing_framework.models.activities import ForEachActivity, SetVariableActivity
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable


def test_when_evaluate_child_activities_then_should_return_the_activity_with_item_expression_evaluated() -> None:
    # Arrange
    test_framework = TestFramework("Fabric")
    for_each_activity = ForEachActivity(
        name="ForEachActivity",
        typeProperties={
            "items": DataFactoryElement("@split('a,b,c', ',')"),
        },
        activities=[
            SetVariableActivity(
                name="setVariable",
                typeProperties={
                    "variableName": "variable",
                    "value": DataFactoryElement("@item()"),
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
    activities = test_framework.evaluate_activity(for_each_activity, state)

    # Assert
    set_variable_activity: SetVariableActivity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"
    assert set_variable_activity.type_properties["value"].result == "a"

    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"
    assert set_variable_activity.type_properties["value"].result == "b"

    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"
    assert set_variable_activity.type_properties["value"].result == "c"

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
