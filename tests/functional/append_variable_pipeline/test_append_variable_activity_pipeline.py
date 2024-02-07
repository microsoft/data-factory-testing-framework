from typing import List

import pytest
from data_factory_testing_framework.models.activities.append_variable_activity import AppendVariableActivity
from data_factory_testing_framework.models.activities.set_variable_activity import SetVariableActivity
from data_factory_testing_framework.state import RunParameter, RunParameterType
from data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


@pytest.mark.parametrize(
    "initial_value,appended_value,expected_value",
    [
        ([1, 2], 3, [1, 2, 3]),
        ([], 1, [1]),
        ([4], 5, [4, 5]),
    ],
)
def test_append_variable_activity(
    initial_value: List[int], appended_value: int, expected_value: List[int], request: pytest.FixtureRequest
) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path=request.fspath.dirname,
        should_evaluate_child_pipelines=True,
    )
    pipeline = test_framework.repository.get_pipeline_by_name("append-variable-test")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [
            RunParameter(RunParameterType.Pipeline, "initial_value", initial_value),
            RunParameter(RunParameterType.Pipeline, "appended_value", appended_value),
        ],
    )

    # Assert
    activity: SetVariableActivity = next(activities)
    assert activity.type == "SetVariable"
    assert activity.value.result == initial_value

    activity: AppendVariableActivity = next(activities)
    assert activity.type == "AppendVariable"
    assert activity.value.result == appended_value
