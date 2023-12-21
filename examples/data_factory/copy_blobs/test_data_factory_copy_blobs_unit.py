import pytest
from data_factory_testing_framework.models.activities.activity import Activity
from data_factory_testing_framework.models.activities.for_each_activity import ForEachActivity
from data_factory_testing_framework.models.pipeline import Pipeline
from data_factory_testing_framework.state import (
    PipelineRunState,
    PipelineRunVariable,
    RunParameter,
    RunParameterType,
)
from data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


@pytest.fixture
def test_framework(request: pytest.FixtureRequest) -> TestFramework:
    return TestFramework(
        framework_type=TestFrameworkType.DataFactory,
        root_folder_path=request.fspath.dirname,
    )


@pytest.fixture
def pipeline(test_framework: TestFramework) -> Pipeline:
    return test_framework.repository.get_pipeline_by_name("copy_blobs")


def test_list_blobs(pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("List Folders")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="SourceContainerName", default_value="source"),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Global, "SourceStorageAccountName", "sourcestorage"),
            RunParameter[str](
                RunParameterType.Pipeline, "SourceContainerName", "container-8b6b545b-c583-4a06-adf7-19ff41370aba"
            ),
            RunParameter[str](RunParameterType.Pipeline, "SourceFolderPrefix", "testfolder"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert activity.name == "List Folders"
    assert (
        activity.type_properties["url"].value
        == "https://sourcestorage.blob.core.windows.net/container-8b6b545b-c583-4a06-adf7-19ff41370aba?restype=container&comp=list&prefix=testfolder&delimiter=$SourceBlobDelimiter"
    )
    assert activity.type_properties["method"] == "GET"


def test_for_each(pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("For Each SourceFolder")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="SourceContainerName", default_value="source"),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Global, "SourceStorageAccountName", "sourcestorage"),
            RunParameter[str](
                RunParameterType.Pipeline, "SourceContainerName", "container-8b6b545b-c583-4a06-adf7-19ff41370aba"
            ),
            RunParameter[str](RunParameterType.Pipeline, "SourceFolderPrefix", "testfolder"),
        ],
    )
    state.add_activity_result(
        activity_name="List Folders",
        status="Succeeded",
        output={
            "Response": """
                    <EnumerationResults ServiceEndpoint="http://myaccount.blob.core.windows.net/"  ContainerName="mycontainer">  
                        <Prefix>testfolder</Prefix>  
                        <Delimiter>$SourceBlobDelimiter</Delimiter>  
                        <Blobs>  
                            <BlobPrefix>
                                <Name>testfolder_1/$SourceBlobDelimiter</Name>
                            </BlobPrefix>
                            <BlobPrefix>
                                <Name>testfolder_2/$SourceBlobDelimiter</Name>
                            </BlobPrefix>
                        </Blobs>
                    </EnumerationResults>
                    """
        },
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert activity.name == "For Each SourceFolder"
    assert activity.type_properties["items"].value == [
        "testfolder_1/$SourceBlobDelimiter",
        "testfolder_2/$SourceBlobDelimiter",
    ]
    assert len(activity.type_properties["activities"]) == 1
    assert activity.type_properties["activities"][0]["name"] == "Copy files to Destination"
    assert activity.type_properties["activities"][0]["type"] == "Copy"


def _get_child_activity_by_name(foreach_activity: ForEachActivity, name: str) -> Activity:
    return next(activity for activity in foreach_activity.activities if activity.name == name)


@pytest.mark.parametrize(
    "wildcardfolderpath",
    [
        ("testfolder_1/$SourceBlobDelimiter"),
        ("testfolder_2/$SourceBlobDelimiter"),
    ],
)
def test_copy_blobs_activity(pipeline: Pipeline, wildcardfolderpath: str) -> None:
    # Arrange
    foreach_activity = pipeline.get_activity_by_name("For Each SourceFolder")
    activity = _get_child_activity_by_name(foreach_activity, "Copy files to Destination")
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.Global, "SourceStorageAccountName", "sourcestorage"),
            RunParameter(
                RunParameterType.Pipeline, "SourceContainerName", "container-8b6b545b-c583-4a06-adf7-19ff41370aba"
            ),
            RunParameter(RunParameterType.Pipeline, "SinkStorageAccountName", "sinkstorage"),
            RunParameter(RunParameterType.Pipeline, "SinkContainerName", "sinkcontainer"),
            RunParameter(RunParameterType.Pipeline, "SinkFolderName", "sinkfolder"),
        ],
        iteration_item=wildcardfolderpath,
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert activity.name == "Copy files to Destination"
    assert activity.type_properties["source"]["storeSettings"]["wildcardFolderPath"].value == wildcardfolderpath
