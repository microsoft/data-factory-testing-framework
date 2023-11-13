import pytest

from data_factory_testing_framework.generated.models import (
    Activity,
    ActivityDependency,
    DataFactoryElement,
    DependencyCondition,
    ExecutePipelineActivity,
    PipelineReference,
    PipelineReferenceType,
)
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState
from data_factory_testing_framework.models.test_framework import TestFramework

TestFramework()


@pytest.mark.parametrize(
    "required_condition, actual_condition, expected",
    [
        ("Succeeded", "Succeeded", True),
        ("Failed", "Succeeded", False),
        ("Skipped", "Succeeded", False),
        ("Completed", "Succeeded", False),
        ("Failed", "Failed", True),
        ("Skipped", "Failed", False),
        ("Completed", "Failed", False),
        ("Skipped", "Skipped", True),
        ("Completed", "Skipped", False),
        ("Completed", "Completed", True),
    ],
)
def test_dependency_conditions_when_called_returns_expected(
    required_condition: str, actual_condition: str, expected: bool
) -> None:
    # Arrange
    pipeline_activity = Activity(
        name="activity",
        depends_on=[
            ActivityDependency(activity="otherActivity", dependency_conditions=[required_condition]),
        ],
    )

    state = PipelineRunState()
    state.add_activity_result("otherActivity", actual_condition)

    # Act
    result = pipeline_activity.are_dependency_condition_met(state)

    # Assert
    assert result == expected


def test_evaluate_when_no_status_is_set_should_set_status_to_succeeded() -> None:
    # Arrange
    pipeline_activity = Activity(name="activity", depends_on=[])
    state = PipelineRunState()

    # Act
    pipeline_activity.evaluate(state)

    # Assert
    assert pipeline_activity.status == DependencyCondition.Succeeded


def test_evaluate_is_evaluating_expressions_inside_dict() -> None:
    # Arrange
    pipeline_activity = ExecutePipelineActivity(
        name="activity",
        pipeline=PipelineReference(type=PipelineReferenceType.PIPELINE_REFERENCE, reference_name="dummy"),
        depends_on=[],
        parameters={
            "url": DataFactoryElement("pipeline().parameters.url"),
        },
    )
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.Pipeline, "url", "example.com"),
        ],
    )

    # Act
    pipeline_activity.evaluate(state)

    # Assert
    assert pipeline_activity.parameters["url"].value == "example.com"
