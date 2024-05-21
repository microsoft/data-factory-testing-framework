import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.models import DataFactoryElement, DataFactoryObjectType
from data_factory_testing_framework.models.activities import ForEachActivity, SetVariableActivity
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable, RunParameter, RunParameterType


def test_when_evaluate_child_activities_then_should_return_the_activity_with_item_expression_evaluated() -> None:
    # Arrange
    test_framework = TestFramework(TestFrameworkType.Fabric)
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


@pytest.mark.parametrize(("evaluated_value"), [1, 1.1, "string-value", {}, True, None])
def test_evaluated_raises_error_when_evaluated_value_is_not_a_list(evaluated_value: DataFactoryObjectType) -> None:
    # Arrange
    state = PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "input_values", evaluated_value)])
    foreach_activity = ForEachActivity(
        name="ForEachActivity",
        typeProperties={
            "items": DataFactoryElement("@pipeline().parameters.input_values"),
        },
        activities=[],
        depends_on=[],
    )

    # Act
    with pytest.raises(ControlActivityExpressionEvaluatedNotToExpectedTypeError) as ex_info:
        foreach_activity.evaluate(state)

    assert (
        ex_info.value.args[0]
        == "Iteration expression of Activity: 'ForEachActivity' does not evaluate to the expected type: 'list'."
    )
