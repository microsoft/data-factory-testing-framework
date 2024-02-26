import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.state import (
    DependencyCondition,
    RunParameter,
    RunParameterType,
)


def test_copy_blobs_pipeline(request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.DataFactory, root_folder_path=request.fspath.dirname
    )
    pipeline = test_framework.get_pipeline_by_name("copy_blobs")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline=pipeline,
        parameters=[
            RunParameter(RunParameterType.Global, "SourceStorageAccountName", "sourcestorageaccount"),
            RunParameter(RunParameterType.Pipeline, "SourceContainerName", "sourcecontainer"),
            RunParameter(RunParameterType.Pipeline, "SourceFolderPrefix", "sourcefolder"),
            RunParameter(RunParameterType.Pipeline, "SinkStorageAccountName", "sinkstorageaccount"),
            RunParameter(RunParameterType.Pipeline, "SinkContainerName", "sinkcontainer"),
            RunParameter(RunParameterType.Pipeline, "SinkFolderName", "sinkfolder"),
        ],
    )

    # Assert
    list_folder_activity = next(activities)
    assert list_folder_activity.name == "List Folders"
    assert (
        list_folder_activity.type_properties["url"].result
        == "https://sourcestorageaccount.blob.core.windows.net/sourcecontainer?restype=container&comp=list&prefix=sourcefolder&delimiter=$SourceBlobDelimiter"
    )
    assert list_folder_activity.type_properties["method"] == "GET"
    list_folder_activity.set_result(
        result=DependencyCondition.SUCCEEDED,
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

    copy_activity = next(activities)

    assert copy_activity.name == "Copy files to Destination"
    assert copy_activity.type == "Copy"
    assert (
        copy_activity.type_properties["source"]["storeSettings"]["wildcardFolderPath"].result
        == "testfolder_1/$SourceBlobDelimiter"
    )

    copy_activity = next(activities)
    assert copy_activity.name == "Copy files to Destination"
    assert copy_activity.type == "Copy"
    assert (
        copy_activity.type_properties["source"]["storeSettings"]["wildcardFolderPath"].result
        == "testfolder_2/$SourceBlobDelimiter"
    )

    pytest.raises(StopIteration, lambda: next(activities))
