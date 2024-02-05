from data_factory_testing_framework.models.activities.execute_pipeline_activity import ExecutePipelineActivity
from data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from data_factory_testing_framework.state import PipelineRunState, RunParameter, RunParameterType


def test_execute_pipeline_activity_evaluates_parameters() -> None:
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
    assert activity.parameters["url"].value == "value1"


def test_execute_pipeline_activity_evaluates_no_parameters() -> None:
    # Arrange
    execute_pipeline_activity = ExecutePipelineActivity(
        name="ExecutePipelineActivity",
        typeProperties={},
        depends_on=[],
    )
    state = PipelineRunState()

    # Act
    activity = execute_pipeline_activity.evaluate(state)

    # Assert
    assert activity is not None
    assert activity.name == "ExecutePipelineActivity"
    assert activity.parameters == {}
