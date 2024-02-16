import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.exceptions.variable_being_evaluated_does_not_exist_error import (
    VariableBeingEvaluatedDoesNotExistError,
)
from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities import SetVariableActivity
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable


def test_when_string_variable_evaluated_then_state_variable_should_be_set() -> None:
    # Arrange
    TestFramework(framework_type=TestFrameworkType.Fabric)
    variable_name = "TestVariable"
    set_variable_activity = SetVariableActivity(
        name="SetVariableActivity",
        typeProperties={
            "variableName": variable_name,
            "value": DataFactoryElement("TestValue"),
        },
    )
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name=variable_name, default_value=""),
        ],
    )

    # Act
    set_variable_activity.evaluate(state)

    # Assert
    variable = state.get_variable_by_name(variable_name)
    assert variable.value == "TestValue"


def test_when_unknown_variable_evaluated_then_should_raise_exception() -> None:
    # Arrange
    TestFramework(framework_type=TestFrameworkType.Fabric)
    variable_name = "TestVariable"
    set_variable_activity = SetVariableActivity(
        name="SetVariableActivity",
        typeProperties={
            "variableName": variable_name,
            "value": DataFactoryElement("TestValue"),
        },
    )
    state = PipelineRunState()

    # Act
    with pytest.raises(VariableBeingEvaluatedDoesNotExistError) as exception_info:
        set_variable_activity.evaluate(state)

    # Assert
    assert exception_info.value.args[0] == "Variable being evaluated does not exist: TestVariable"
