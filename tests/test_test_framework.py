import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.exceptions import (
    NoRemainingPipelineActivitiesMeetDependencyConditionsError,
)
from data_factory_testing_framework.models import DataFactoryElement, Pipeline
from data_factory_testing_framework.models.activities import FailActivity, SetVariableActivity


def test_circular_dependency_between_activities_should_throw_error() -> None:
    # Arrange
    test_framework = TestFramework(TestFrameworkType.Fabric)
    pipeline = Pipeline(
        id_="some-id",
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
    test_framework._repository.pipelines.append(pipeline)

    # Act & Assert
    with pytest.raises(NoRemainingPipelineActivitiesMeetDependencyConditionsError):
        next(test_framework.evaluate_pipeline(pipeline, []))


def test_fail_activity_halts_further_evaluation() -> None:
    # Arrange
    test_framework = TestFramework(TestFrameworkType.Fabric)
    pipeline = Pipeline(
        id_="some-id",
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
    test_framework._repository.pipelines.append(pipeline)

    # Act
    activities = test_framework.evaluate_pipeline(pipeline, [])

    # Assert
    activity = next(activities)
    assert activity is not None
    assert activity.name == "failActivity"
    assert activity.type == "Fail"
    assert activity.status == "Failed"
    assert activity.type_properties["message"].result == "Error code: 500"
    assert activity.type_properties["errorCode"] == "500"

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
