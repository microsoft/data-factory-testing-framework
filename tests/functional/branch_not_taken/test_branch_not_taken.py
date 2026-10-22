import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.state import RunParameter, RunParameterType


@pytest.mark.parametrize(
    "date,expected_activity_name,expected_day",
    [
        ("", "Set_Today", None),
        ("2024-01-31T00:00:00Z", "Set_Given_Date", "2024-01-31"),
    ],
)
def test_if_condition_only_evaluates_the_branch_taken(
    date: str,
    expected_activity_name: str,
    expected_day: str,
    request: pytest.FixtureRequest,
) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.DataFactory,
        root_folder_path=request.fspath.dirname,
    )
    pipeline = test_framework.get_pipeline_by_name("if_condition_branch")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [
            RunParameter(RunParameterType.Pipeline, "date", date),
        ],
    )

    # Assert
    activity = next(activities)
    assert activity.name == expected_activity_name
    if expected_day is not None:
        assert activity.type_properties["value"].result == expected_day

    with pytest.raises(StopIteration):
        next(activities)


@pytest.mark.parametrize(
    "mode,date,expected_activity_name",
    [
        ("today", "", "Set_Today"),
        ("given", "2024-01-31T00:00:00Z", "Set_Given_Date"),
    ],
)
def test_switch_only_evaluates_the_case_taken(
    mode: str,
    date: str,
    expected_activity_name: str,
    request: pytest.FixtureRequest,
) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.DataFactory,
        root_folder_path=request.fspath.dirname,
    )
    pipeline = test_framework.get_pipeline_by_name("switch_default_branch")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [
            RunParameter(RunParameterType.Pipeline, "mode", mode),
            RunParameter(RunParameterType.Pipeline, "date", date),
        ],
    )

    # Assert
    activity = next(activities)
    assert activity.name == expected_activity_name

    with pytest.raises(StopIteration):
        next(activities)
