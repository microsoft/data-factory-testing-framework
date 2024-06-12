import os
from pathlib import Path

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.models import Pipeline
from data_factory_testing_framework.models.activities import IfConditionActivity
from data_factory_testing_framework.state import (
    PipelineRunState,
)


@pytest.fixture
def test_framework(request: pytest.FixtureRequest) -> TestFramework:
    return TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path=os.path.join(Path(request.fspath.dirname).parent),
    )


@pytest.fixture
def pipeline(test_framework: TestFramework) -> Pipeline:
    return test_framework.get_pipeline_by_name("pl_main")


def test_activity_read_configuration_file(request: pytest.FixtureRequest, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Read Configuration File")

    # Act
    state = PipelineRunState()
    activity.evaluate(state)

    # Assert
    expected_data_store_type = "Lakehouse"
    assert (
        expected_data_store_type == (activity.type_properties["datasetSettings"]["linkedService"]["properties"]["type"])
    )

    expected_file_name = "lh_config.json"
    assert expected_file_name == (activity.type_properties["datasetSettings"]["typeProperties"]["location"]["fileName"])

    expected_folder_name = "config"
    assert (
        expected_folder_name
        == (activity.type_properties["datasetSettings"]["typeProperties"]["location"]["folderPath"])
    )


def test_activity_if_true(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    foreach_activity = pipeline.get_activity_by_name("ForEachYearMonthPair")
    child_activity: IfConditionActivity = next(
        filter(lambda a: a.name == "If New Or Updated", foreach_activity.activities)
    )

    # Act
    state = PipelineRunState(
        iteration_item={
            "year": "2019",
            "month": "09",
            "created": "2023-05-24T11:04:42Z",
            "lastUpdatedSourceSystem": "2023-05-24T11:04:42Z",
            "lastUpdatedDatalake": "2023-05-01T11:04:42Z",
        }
    )

    child_activity.evaluate(state)

    # Assert
    assert child_activity.type_properties["expression"].result is True

def test_activity_if_false(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    foreach_activity = pipeline.get_activity_by_name("ForEachYearMonthPair")
    child_activity: IfConditionActivity = next(
        filter(lambda a: a.name == "If New Or Updated", foreach_activity.activities)
    )

    # Act
    state = PipelineRunState(
        iteration_item={
            "year": "2019",
            "month": "09",
            "created": "2023-05-24T11:04:42Z",
            "lastUpdatedSourceSystem": "2023-05-24T11:04:42Z",
            "lastUpdatedDatalake": "2023-05-25T11:04:42Z",
        }
    )

    child_activity.evaluate(state)

    # Assert
    assert child_activity.type_properties["expression"].result is False


def test_activity_invoke_pipeline(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    foreach_activity = pipeline.get_activity_by_name("ForEachYearMonthPair")
    if_activity: IfConditionActivity = next(
        filter(lambda a: a.name == "If New Or Updated", foreach_activity.activities)
    )

    inner_pipeline_activity = next(
        filter(lambda a: a.name == "Invoke Ingestion Pipeline", if_activity.if_true_activities)
    )

    # Act
    state = PipelineRunState(
        iteration_item={
            "year": "2019",
            "month": "09",
            "created": "2023-05-24T11:04:42Z",
            "lastUpdatedSourceSystem": "2023-24-01T11:04:42Z",
            "lastUpdatedDatalake": "2023-05-24T11:04:42Z",
        }
    )
    inner_pipeline_activity.evaluate(state)

    # Assert
    assert (
        inner_pipeline_activity.type_properties["pipeline"]["referenceName"] == "f2a51fa4-bd34-4b81-86a5-9c88a446415f"
    )
    assert inner_pipeline_activity.type_properties["parameters"]["dynamicmonth"].result == "09"
    assert inner_pipeline_activity.type_properties["parameters"]["dynamicyear"].result == "2019"
