import pytest

from azure_data_factory_testing_framework.data_factory import TestFramework
from azure_data_factory_testing_framework.data_factory.generated.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.data_factory.generated.models import (
    ActivityDependency,
    PipelineResource,
    SetVariableActivity,
)
from azure_data_factory_testing_framework.exceptions.pipeline_activities_circular_dependency_error import (
    PipelineActivitiesCircularDependencyError,
)


def test_circular_dependency_between_activities_should_throw_error() -> None:
    # Arrange
    test_framework = TestFramework()
    pipeline = PipelineResource(
        name="main",
        parameters={},
        activities=[
            SetVariableActivity(
                name="setVariable1",
                variable_name="variable",
                value=DataFactoryElement[str]("'1'"),
                depends_on=[
                    ActivityDependency(activity="setVariable2", dependency_conditions=["Succeeded"]),
                ],
            ),
            SetVariableActivity(
                name="setVariable2",
                variable_name="variable",
                value=DataFactoryElement[str]("'1'"),
                depends_on=[
                    ActivityDependency(activity="setVariable1", dependency_conditions=["Succeeded"]),
                ],
            ),
        ],
    )
    test_framework.repository.pipelines.append(pipeline)

    # Act & Assert
    with pytest.raises(PipelineActivitiesCircularDependencyError):
        next(test_framework.evaluate_pipeline(pipeline, []))
