import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.models import DataFactoryElement, Pipeline
from data_factory_testing_framework.models.activities import FilterActivity
from data_factory_testing_framework.state import RunParameter, RunParameterType


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
def test_filter_activity_on_range_of_values(input_values: [], expected_filtered_values: []) -> None:
    # Arrange
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric)
    pipeline = Pipeline(
        id_="some-id",
        name="pipeline",
        parameters={
            "input_values": {
                "type": "Array",
                "defaultValue": [],
            },
        },
        variables={},
        activities=[
            FilterActivity(
                name="FilterActivity",
                typeProperties={
                    "items": DataFactoryElement("@pipeline().parameters.input_values"),
                    "condition": DataFactoryElement("@lessOrEquals(item(), 3)"),
                },
            ),
        ],
    )

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [
            RunParameter(RunParameterType.Pipeline, "input_values", input_values),
        ],
    )

    # Assert
    activity = next(activities)
    assert activity.type == "Filter"
    assert activity.type_properties["items"].result == input_values
    assert activity.output["value"] == expected_filtered_values
