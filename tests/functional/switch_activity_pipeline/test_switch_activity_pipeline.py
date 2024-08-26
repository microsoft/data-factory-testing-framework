import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.state import RunParameter, RunParameterType


@pytest.mark.parametrize(
    "on_value,expected_outcome",
    [
        ("case_1", "case_1_hit"),
        ("case_2", "case_2_hit"),
        ("case_3", "default_hit"),
        ("case_4", "default_hit"),
        ("case_anything", "default_hit"),
    ],
)
def test_switch_activity(on_value: str, expected_outcome: str, request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.DataFactory,
        root_folder_path=request.fspath.dirname,
        should_evaluate_child_pipelines=True,
    )
    pipeline = test_framework.get_pipeline_by_name("switchtest")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [
            RunParameter(RunParameterType.Pipeline, "current_value", on_value),
        ],
    )

    # Assert
    activity = next(activities)
    assert activity.type == "SetVariable"
    assert activity.type_properties["value"] == expected_outcome
