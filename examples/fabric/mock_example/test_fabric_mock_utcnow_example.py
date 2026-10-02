from pathlib import Path

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.mock_helpers import mock_utcnow


def test_mock_utcnow_single_value(request: pytest.FixtureRequest) -> None:
    # Arrange
    fabric_folder = Path(request.fspath.dirname, "fabric")
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric, root_folder_path=fabric_folder)
    pipeline = test_framework.get_pipeline_by_name("ExamplePipeline")

    # Create a global mock for utcnow
    utcnow_mock = mock_utcnow("1990-05-12T10:30:00Z")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        parameters=[],
        mocks=[utcnow_mock],
    )

    # Assert
    activity = next(activities)

    assert activity.type_properties["value"].result == ["1990-05-12T10:30:00Z", "1990-05-12T10:30:00Z"]

    activity = next(activities)
    # note: we ignore the assertions here for the purpose of this example

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)

def test_mock_utcnow_multiple_values(request: pytest.FixtureRequest) -> None:
    # Arrange
    fabric_folder = Path(request.fspath.dirname, "fabric")
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric, root_folder_path=fabric_folder)
    pipeline = test_framework.get_pipeline_by_name("ExamplePipeline")

    # Create a global mock for utcnow
    utcnow_mock = mock_utcnow(
        [
            "1980-05-12T10:30:00Z",
            "1990-05-12T10:30:00Z",
        ]
    )

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        parameters=[],
        mocks=[utcnow_mock],
    )

    # Assert
    activity = next(activities)
    assert activity.type_properties["value"].result == ["1980-05-12T10:30:00Z", "1990-05-12T10:30:00Z"]

    activity = next(activities)
    # note: we ignore the assertions here for the purpose of this example

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)

def test_mock_utcnow_with_activity_scope(request: pytest.FixtureRequest) -> None:
    # Arrange
    fabric_folder = Path(request.fspath.dirname, "fabric")
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric, root_folder_path=fabric_folder)
    pipeline = test_framework.get_pipeline_by_name("ExamplePipeline")

    # Create a mock for utcnow with activity scope
    utcnow_mock = mock_utcnow("1980-05-12T10:30:00Z", activity="Set Input Data")
    utcnow_mock_set_addtional_input = mock_utcnow("1990-05-12T10:30:00Z", activity="Set Additional Input Data")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        parameters=[],
        mocks=[
            utcnow_mock,
            utcnow_mock_set_addtional_input
        ],
    )

    # Assert
    activity = next(activities)
    assert activity.type_properties["value"].result == ["1980-05-12T10:30:00Z", "1980-05-12T10:30:00Z"]

    activity = next(activities)
    assert activity.type_properties["value"].result == ["1990-05-12T10:30:00Z", "1990-05-12T10:30:00Z"]

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)

def test_mock_utcnow_with_scope_different_pipeline(request: pytest.FixtureRequest) -> None:

    # TODO: create a nested pipeline to test the scope functionality
    # Need a nested pipeline to test the scope functionality

    pass


