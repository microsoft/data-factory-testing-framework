from pathlib import Path

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType


def test_simple_web_hook(request: pytest.FixtureRequest) -> None:
    # Arrange
    fabric_folder = Path(request.fspath.dirname, "fabric")
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric, root_folder_path=fabric_folder)
    pipeline = test_framework.get_pipeline_by_name("ExamplePipeline")

    # Act
    activities = test_framework.evaluate_pipeline(pipeline, [])

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
