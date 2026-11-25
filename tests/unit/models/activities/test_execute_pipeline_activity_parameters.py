from data_factory_testing_framework.models import DataFactoryElement
from data_factory_testing_framework.models._pipeline import Pipeline
from data_factory_testing_framework.models.activities import ExecutePipelineActivity
from data_factory_testing_framework.state import PipelineRunState, RunParameter, RunParameterType


def test_execute_pipeline_activity_evaluates_parameters(
    pipeline: Pipeline,
) -> None:
    # Arrange
    execute_pipeline_activity = ExecutePipelineActivity(
        name="ExecutePipelineActivity",
        typeProperties={
            "parameters": {
                "url": DataFactoryElement("@pipeline().parameters.param1"),
            },
        },
        depends_on=[],
    )
    execute_pipeline_activity._pipeline = pipeline

    state = PipelineRunState(
        parameters=[
            RunParameter(name="param1", value="value1", parameter_type=RunParameterType.Pipeline),
        ],
    )

    # Act
    activity = execute_pipeline_activity.evaluate(state)

    # Assert
    assert activity is not None
    assert activity.name == "ExecutePipelineActivity"
    assert activity.parameters["url"].result == "value1"


def test_execute_pipeline_activity_evaluates_no_parameters(
    pipeline: Pipeline,
) -> None:
    # Arrange
    execute_pipeline_activity = ExecutePipelineActivity(
        name="ExecutePipelineActivity",
        typeProperties={},
        depends_on=[],
    )
    execute_pipeline_activity._pipeline = pipeline

    state = PipelineRunState()

    # Act
    activity = execute_pipeline_activity.evaluate(state)

    # Assert
    assert activity is not None
    assert activity.name == "ExecutePipelineActivity"
    assert activity.parameters == {}
