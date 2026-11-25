import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.mock_helpers import mock_utcnow
from pathlib import Path

def test_mock_utcnow_example(request: pytest.FixtureRequest) -> None:
    # Arrange
    fabric_folder = Path(request.fspath.dirname, "fabric")
    test_framework = TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path=fabric_folder
    )
    pipeline = test_framework.get_pipeline_by_name("ExamplePipeline")

    # Create a global mock for utcnow
    utcnow_mock = mock_utcnow("2025-05-12T10:30:00Z")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        parameters=[],
        mocks=[utcnow_mock],
    )

    # Assert
    activity = next(activities)
    assert activity.name == "Set Input Data"

    activity = next(activities)
    assert activity.name == "Call Webhook"

    activity = next(activities)
    assert activity.name == "Call Webhook"

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
