from typing import List

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.exceptions import (
    VariableBeingEvaluatedDoesNotExistError,
)
from data_factory_testing_framework.models import DataFactoryElement
from data_factory_testing_framework.models.activities import AppendVariableActivity
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable


@pytest.mark.parametrize(
    "initial_value,appended_value,expected_value",
    [
        ([1, 2], 3, [1, 2, "3"]),
        ([], 1, ["1"]),
        ([4], 5, [4, "5"]),
    ],
)
def test_when_int_variable_appended_then_state_variable_should_be_set(
    initial_value: List[int], appended_value: int, expected_value: List[int]
) -> None:
    # Arrange
    TestFramework(framework_type=TestFrameworkType.Fabric)
    variable_name = "TestVariable"
    set_variable_activity = AppendVariableActivity(
        name="AppendVariableActivity",
        typeProperties={
            "variableName": variable_name,
            "value": DataFactoryElement(str(appended_value)),
        },
    )
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name=variable_name, default_value=initial_value),
        ],
    )

    # Act
    set_variable_activity.evaluate(state)

    # Assert
    variable = state.get_variable_by_name(variable_name)
    assert variable.value == expected_value


def test_when_unknown_variable_evaluated_then_should_raise_exception() -> None:
    # Arrange
    TestFramework(framework_type=TestFrameworkType.Fabric)
    variable_name = "TestVariable"
    set_variable_activity = AppendVariableActivity(
        name="AppendVariableActivity",
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
