import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType


def test_fabric_supports_utf_16_le_encoded_pipeline_content(request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path=request.fspath.dirname,
        should_evaluate_child_pipelines=True,
    )

    # Act
    pipeline = test_framework.get_pipeline_by_name("utf_16_encoding")

    # Assert
    assert pipeline is not None
    assert pipeline.name == "utf_16_encoding"
