import pytest

from data_factory_testing_framework.exceptions.variable_being_evaluated_does_not_exist_error import (
    VariableBeingEvaluatedDoesNotExistError,
)
from data_factory_testing_framework.generated.models import (
    DataFactoryElement,
    SetVariableActivity,
    VariableSpecification,
)
from data_factory_testing_framework.state import PipelineRunState
from data_factory_testing_framework.test_framework import TestFramework


def test_when_string_variable_evaluated_then_state_variable_should_be_set() -> None:
    # Arrange
    TestFramework()
    variable_name = "TestVariable"
    set_variable_activity = SetVariableActivity(
        name="SetVariableActivity",
        variable_name=variable_name,
        value=DataFactoryElement("TestValue"),
    )
    state = PipelineRunState(
        variable_specifications={
            variable_name: VariableSpecification(type="String", default_value=""),
        },
    )

    # Act
    set_variable_activity.evaluate(state)

    # Assert
    variable = state.get_variable_by_name(variable_name)
    assert variable.value == "TestValue"


def test_when_unknown_variable_evaluated_then_should_raise_exception() -> None:
    # Arrange
    TestFramework()
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
