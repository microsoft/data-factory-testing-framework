import pytest
from azure_data_factory_testing_framework.exceptions.pipeline_activities_circular_dependency_error import (
    PipelineActivitiesCircularDependencyError,
)
from azure_data_factory_testing_framework.models.activities.fail_activity import FailActivity
from azure_data_factory_testing_framework.models.activities.set_variable_activity import SetVariableActivity
from azure_data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.models.pipeline import Pipeline
from azure_data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


def test_circular_dependency_between_activities_should_throw_error() -> None:
    # Arrange
    test_framework = TestFramework(TestFrameworkType.Fabric)
    pipeline = Pipeline(
        name="main",
        parameters={},
        variables={},
        activities=[
            SetVariableActivity(
                name="setVariable1",
                variable_name="variable",
                typeProperties={
                    "variableName": "variable",
                    "value": DataFactoryElement("'1'"),
                },
                dependsOn=[
                    {
                        "activity": "setVariable2",
                        "dependencyConditions": [
                            "Succeeded",
                        ],
                    }
                ],
            ),
            SetVariableActivity(
                name="setVariable2",
                variable_name="variable",
                typeProperties={
                    "variableName": "variable",
                    "value": DataFactoryElement("'1'"),
                },
                dependsOn=[
                    {
                        "activity": "setVariable1",
                        "dependencyConditions": [
                            "Succeeded",
                        ],
                    }
                ],
            ),
        ],
    )
    test_framework.repository.pipelines.append(pipeline)

    # Act & Assert
    with pytest.raises(PipelineActivitiesCircularDependencyError):
        next(test_framework.evaluate_pipeline(pipeline, []))


def test_fail_activity_halts_further_evaluation() -> None:
    # Arrange
    test_framework = TestFramework(TestFrameworkType.Fabric)
    pipeline = Pipeline(
        name="main",
        parameters={},
        variables={},
        activities=[
            SetVariableActivity(
                name="setVariable1",
                variable_name="variable",
                typeProperties={
                    "variableName": "variable",
                    "value": DataFactoryElement("'1'"),
                },
                dependsOn=[
                    {
                        "activity": "failActivity",
                        "dependencyConditions": [
                            "Succeeded",
                        ],
                    }
                ],
            ),
            FailActivity(
                name="failActivity",
                typeProperties={
                    "message": DataFactoryElement("@concat('Error code: ', '500')"),
                    "errorCode": "500",
                },
                dependsOn=[],
            ),
        ],
    )
    test_framework.repository.pipelines.append(pipeline)

    # Act
    activities = test_framework.evaluate_pipeline(pipeline, [])

    # Assert
    activity = next(activities)
    assert activity is not None
    assert activity.name == "failActivity"
    assert activity.type == "Fail"
    assert activity.status == "Failed"
    assert activity.type_properties["message"].value == "Error code: 500"
    assert activity.type_properties["errorCode"] == "500"

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
