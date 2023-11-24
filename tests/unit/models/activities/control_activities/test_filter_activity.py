from azure_data_factory_testing_framework.models.activities.filter_activity import FilterActivity
from azure_data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.models.pipeline import Pipeline
from azure_data_factory_testing_framework.state import RunParameter, RunParameterType
from azure_data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


def test_filter_activity_on_range_of_values() -> None:
    # Arrange
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric)
    pipeline = Pipeline(
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
            RunParameter(RunParameterType.Pipeline, "input_values", [1, 2, 3, 4, 5]),
        ],
    )

    # Assert
    activity = next(activities)
    assert activity.type == "Filter"
    assert activity.type_properties["items"].value == [1, 2, 3, 4, 5]
    assert activity.output["value"] == [1, 2, 3]
