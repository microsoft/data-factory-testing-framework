import os
from pathlib import Path

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.models import Pipeline
from data_factory_testing_framework.state import DependencyCondition, RunParameter, RunParameterType


@pytest.fixture
def test_framework(request: pytest.FixtureRequest) -> TestFramework:
    return TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path=os.path.join(Path(request.fspath.dirname).parent),
        should_evaluate_child_pipelines=False,
    )


@pytest.fixture
def pipeline(test_framework: TestFramework) -> Pipeline:
    return test_framework.get_pipeline_by_name("pl_main")


def test_pl_main_pipeline(test_framework: TestFramework) -> None:
    # Arrange
    pipeline = test_framework.get_pipeline_by_name("pl_main")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        parameters=[
            RunParameter(RunParameterType.Pipeline, name="dynamicmonth", value="09"),
            RunParameter(RunParameterType.Pipeline, name="dynamicyear", value="2019"),
        ],
    )

    # Assert pipeline general information
    assert pipeline.name == "pl_main"
    assert len(pipeline.activities) == 2

    # Assert pipeline activities information
    # Activity: Read Configuration File
    read_configuration_file_activity = next(activities)
    assert read_configuration_file_activity.name == "Read Configuration File"
    assert read_configuration_file_activity.type == "Lookup"
    assert (
        read_configuration_file_activity.type_properties["datasetSettings"]["linkedService"]["properties"]["type"]
        == "Lakehouse"
    )
    assert (
        read_configuration_file_activity.type_properties["datasetSettings"]["typeProperties"]["location"]["fileName"]
        == "lh_config.json"
    )
    assert (
        read_configuration_file_activity.type_properties["datasetSettings"]["typeProperties"]["location"]["folderPath"]
        == "config"
    )

    # In order to simulate how the activity would look like when the ForEach activity iterates through the first row
    # the result of the activity needs to be set upfront.
    # Because of the following expression: "@activity('Read Configuration File').output.firstRow.lakeHouseProperties",
    # we need to add the "lakeHouseProperties" and "firstRow" key to the result because the Framework is unaware of these.
    # For the activity test (test_pl_main_activity.py) we just use the inner properties .{"year:"2019","month":"09", ...}.
    # If you are unaware of how the activity result should look like, you can run the pipeline and check the output of the activity.
    read_configuration_file_activity.set_result(
        DependencyCondition.SUCCEEDED,
        {
            "firstRow": {
                "lakeHouseProperties": [
                    {
                        "year": "2019",
                        "month": "09",
                        "created": "2023-05-24T11:04:42Z",
                        "lastUpdatedSourceSystem": "2023-05-24T11:04:42Z",
                        "lastUpdatedDatalake": "2023-05-01T11:04:42Z",
                    }
                ]
            }
        },
    )

    # Next activity is: Invoke Ingestion Pipeline - because for the previous control activities:
    # If and ForEach the framework does the evaluation in the background and
    # it doesn't need to be done manually.
    # With that, the next activity to be evaluated is the Invoke Ingestion Pipeline.

    # Use the following code if your should_evaluate_child_pipelines is set to False
    invoke_ingestion_pipeline_activity = next(activities)
    assert invoke_ingestion_pipeline_activity.name == "Invoke Ingestion Pipeline"
    assert invoke_ingestion_pipeline_activity.type == "ExecutePipeline"
    assert (
        invoke_ingestion_pipeline_activity.type_properties["pipeline"]["referenceName"]
        == "f2a51fa4-bd34-4b81-86a5-9c88a446415f"
    )
    assert invoke_ingestion_pipeline_activity.type_properties["parameters"]["dynamicmonth"].result == "09"
    assert invoke_ingestion_pipeline_activity.type_properties["parameters"]["dynamicyear"].result == "2019"

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
