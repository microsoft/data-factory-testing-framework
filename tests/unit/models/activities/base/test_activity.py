import pytest
from data_factory_testing_framework._test_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.models.activities.activity import Activity
from data_factory_testing_framework.models.activities.execute_pipeline_activity import ExecutePipelineActivity
from data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from data_factory_testing_framework.state import PipelineRunState, RunParameterType
from data_factory_testing_framework.state.dependency_condition import DependencyCondition
from data_factory_testing_framework.state.run_parameter import RunParameter

TestFramework(framework_type=TestFrameworkType.Fabric)


@pytest.mark.parametrize(
    "required_condition, actual_condition, expected",
    [
        ("Succeeded", "Succeeded", True),
        ("Failed", "Succeeded", False),
        ("Skipped", "Succeeded", False),
        ("Completed", "Succeeded", True),
        ("Failed", "Failed", True),
        ("Skipped", "Failed", False),
        ("Completed", "Failed", True),
        ("Skipped", "Skipped", True),
        ("Completed", "Skipped", True),
        ("Completed", "Completed", True),
    ],
)
def test_dependency_conditions_when_called_returns_expected(
    required_condition: str,
    actual_condition: str,
    expected: bool,
) -> None:
    # Arrange
    pipeline_activity = Activity(
        name="activity",
        type="WebActivity",
        dependsOn=[
            {
                "activity": "otherActivity",
                "dependencyConditions": [required_condition],
            }
        ],
    )

    state = PipelineRunState()
    state.add_activity_result("otherActivity", actual_condition)

    # Act
    result = pipeline_activity.are_dependency_condition_met(state)

    # Assert
    assert result == expected


def test_dependency_condition_completed_is_false_when_no_activity_result_is_set() -> None:
    # Arrange
    pipeline_activity = Activity(
        name="activity",
        type="WebActivity",
        dependsOn=[
            {
                "activity": "otherActivity",
                "dependencyConditions": ["Completed"],
            }
        ],
    )
    state = PipelineRunState()

    # Act
    result = pipeline_activity.are_dependency_condition_met(state)

    # Assert
    assert result is False


def test_evaluate_when_no_status_is_set_should_set_status_to_succeeded() -> None:
    # Arrange
    pipeline_activity = Activity(name="activity", type="WebActivity", dependsOn=[])
    state = PipelineRunState()

    # Act
    pipeline_activity.evaluate(state)

    # Assert
    assert pipeline_activity.status == DependencyCondition.Succeeded


def test_evaluate_is_evaluating_expressions_inside_dict() -> None:
    # Arrange
    pipeline_activity = ExecutePipelineActivity(
        name="activity",
        typeProperties={
            "pipeline": {"referenceName": "dummy"},
            "parameters": {
                "url": DataFactoryElement("@pipeline().parameters.url"),
            },
        },
        depends_on=[],
    )
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.Pipeline, "url", "example.com"),
        ],
    )

    # Act
    pipeline_activity.evaluate(state)

    # Assert
    assert pipeline_activity.type_properties["parameters"]["url"].result == "example.com"
