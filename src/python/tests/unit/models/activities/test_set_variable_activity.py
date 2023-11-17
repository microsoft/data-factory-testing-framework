import pytest

from azure_data_factory_testing_framework.data_factory.data_factory_test_framework import DataFactoryTestFramework
from azure_data_factory_testing_framework.data_factory.generated.models import (
    DataFactoryElement,
    SetVariableActivity,
)
from azure_data_factory_testing_framework.exceptions.variable_being_evaluated_does_not_exist_error import (
    VariableBeingEvaluatedDoesNotExistError,
)
from azure_data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable


def test_when_string_variable_evaluated_then_state_variable_should_be_set() -> None:
    # Arrange
    DataFactoryTestFramework()
    variable_name = "TestVariable"
    set_variable_activity = SetVariableActivity(
        name="SetVariableActivity",
        variable_name=variable_name,
        value=DataFactoryElement("TestValue"),
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
    DataFactoryTestFramework()
    variable_name = "TestVariable"
    set_variable_activity = SetVariableActivity(
        name="SetVariableActivity",
        variable_name=variable_name,
        value=DataFactoryElement("TestValue"),
    )
    state = PipelineRunState()

    # Act
    with pytest.raises(VariableBeingEvaluatedDoesNotExistError) as exception_info:
        set_variable_activity.evaluate(state)

    # Assert
    assert exception_info.value.args[0] == "Variable being evaluated does not exist: TestVariable"
