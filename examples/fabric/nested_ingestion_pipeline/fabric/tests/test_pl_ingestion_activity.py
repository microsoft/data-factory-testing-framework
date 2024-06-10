import os
from pathlib import Path

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.models import Pipeline
from data_factory_testing_framework.state import (
    PipelineRunState,
    RunParameter,
    RunParameterType,
)


@pytest.fixture
def test_framework(request: pytest.FixtureRequest) -> TestFramework:
    return TestFramework(
        framework_type=TestFrameworkType.Fabric,
        # root_folder_path = os.path.join(Path(__file__).parent,"pl_ingestion.DataPipeline")
        root_folder_path=os.path.join(Path(request.fspath.dirname).parent, "pl_ingestion.DataPipeline"),
    )


@pytest.fixture
def pipeline(test_framework: TestFramework) -> Pipeline:
    return test_framework.get_pipeline_by_name("pl_ingestion")


def test_copy_nyc_data_to_adls2(pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Copy NYCData to ADLS")
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.Pipeline, name="dynamicmonth", value="01"),
            RunParameter(RunParameterType.Pipeline, name="dynamicyear", value="2023"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert (
        activity.type_properties["source"]["datasetSettings"]["typeProperties"]["location"]["relativeUrl"].result
        == "yellow_tripdata_2023-01.parquet"
    )
    assert (
        activity.type_properties["sink"]["datasetSettings"]["typeProperties"]["location"]["fileName"].result
        == "yellow_tripdata_2023-01.parquet"
    )
    assert (
        activity.type_properties["sink"]["datasetSettings"]["typeProperties"]["location"]["folderPath"].result
        == "nyc_taxi_data/2023/01"
    )


def test_copy_nyc_data_to_lakehouse(pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Copy NYCData to Lakehouse")
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.Pipeline, name="dynamicmonth", value="01"),
            RunParameter(RunParameterType.Pipeline, name="dynamicyear", value="2023"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert (
        activity.type_properties["source"]["datasetSettings"]["typeProperties"]["location"]["fileSystem"]
        == "nyctaxidata"
    )
    assert (
        activity.type_properties["source"]["datasetSettings"]["typeProperties"]["location"]["folderPath"].result
        == "2023/01"
    )
    assert (
        activity.type_properties["source"]["datasetSettings"]["typeProperties"]["location"]["fileName"].result
        == "yellow_tripdata_2023-01.parquet"
    )
    assert (
        activity.type_properties["sink"]["datasetSettings"]["typeProperties"]["location"]["fileName"].result
        == "yellow_tripdata_2023-01.parquet"
    )
    assert (
        activity.type_properties["sink"]["datasetSettings"]["typeProperties"]["location"]["folderPath"].result
        == "nyc_taxi_data/2023/01"
    )
