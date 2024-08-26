import os

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType


@pytest.mark.parametrize(
    "framework_type, example_folder, pipeline_id",
    [
        (TestFrameworkType.DataFactory, "data_factory", "default_variables"),
        (TestFrameworkType.Synapse, "synapse", "set_date"),
        (TestFrameworkType.Fabric, "fabric", "c7986cc7-a6df-45fc-b4b6-dfc3cbddf2a6"),
    ],
)
def test_initializing_test_framework_should_set_framework_type_and_repository(
    framework_type: TestFrameworkType, example_folder: str, pipeline_id: str, request: pytest.FixtureRequest
) -> None:
    # Arrange & Act
    root_folder_path = os.path.join(request.fspath.dirname, "data", example_folder)
    test_framework = TestFramework(framework_type, root_folder_path=root_folder_path)

    # Assert
    assert test_framework._framework_type == framework_type
    assert test_framework._repository is not None
    assert len(test_framework._repository.pipelines) == 1
    assert test_framework._repository.pipelines[0].pipeline_id == pipeline_id
