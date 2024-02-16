import pytest
from data_factory_testing_framework._test_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.models.activities.set_variable_activity import SetVariableActivity
from data_factory_testing_framework.models.activities.until_activity import UntilActivity
from data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable


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
