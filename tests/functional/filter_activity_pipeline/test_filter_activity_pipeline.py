import pytest
from data_factory_testing_framework.models.activities.activity import Activity
from data_factory_testing_framework.models.activities.filter_activity import FilterActivity
from data_factory_testing_framework.state import RunParameter, RunParameterType
from data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


@pytest.mark.parametrize(
    "input_values,expected_filtered_values",
    [
        ([1, 2, 3, 4, 5], [1, 2, 3]),
        ([], []),
        ([4], []),
        ([3, 4, 5, 6], [3]),
        ([4, 5, 6], []),
        ([-1, 3, 4], [-1, 3]),
    ],
)
def test_filter_activity(input_values: [], expected_filtered_values: [], request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path=request.fspath.dirname,
        should_evaluate_child_pipelines=True,
    )
    pipeline = test_framework.repository.get_pipeline_by_name("filter-test")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [
            RunParameter(RunParameterType.Pipeline, "input_values", input_values),
        ],
    )

    # Assert
    activity: FilterActivity = next(activities)
    assert activity.type == "Filter"
    assert activity.items.value == input_values
    assert activity.output["value"] == expected_filtered_values

    activity: Activity = next(activities)
    assert activity.type == "SetVariable"
    assert activity.type_properties["value"].value == expected_filtered_values
