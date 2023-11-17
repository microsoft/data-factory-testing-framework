import pytest

from azure_data_factory_testing_framework.data_factory.data_factory_test_framework import DataFactoryTestFramework
from azure_data_factory_testing_framework.data_factory.generated.models import ParameterSpecification, PipelineResource
from azure_data_factory_testing_framework.state import RunParameterType
from azure_data_factory_testing_framework.state.run_parameter import RunParameter

DataFactoryTestFramework()


def test_when_validate_parameters_is_accurate_should_pass() -> None:
    # Arrange
    pipeline = PipelineResource(
        name="pipeline",
        parameters={
            "pipelineParameterName": ParameterSpecification(type=RunParameterType.Pipeline),
            "pipelineParameterName2": ParameterSpecification(type=RunParameterType.Pipeline),
        },
    )

    # Act
    pipeline.validate_parameters(
        [
            RunParameter(RunParameterType.Pipeline, "pipelineParameterName", "pipelineParameterValue"),
            RunParameter(RunParameterType.Pipeline, "pipelineParameterName2", "pipelineParameterValue2"),
        ],
    )


def test_when_validate_parameters_is_missing_run_parameter_should_throw_error() -> None:
    # Arrange
    pipeline = PipelineResource(
        parameters={
            "pipelineParameterName": ParameterSpecification(type=RunParameterType.Pipeline),
            "pipelineParameterName2": ParameterSpecification(type=RunParameterType.Pipeline),
        },
    )
    pipeline.name = "pipeline"

    # Act
    with pytest.raises(ValueError) as exception_info:
        pipeline.validate_parameters(
            [
                RunParameter(RunParameterType.Pipeline, "pipelineParameterName", "pipelineParameterValue"),
            ],
        )

    # Assert
    assert (
        exception_info.value.args[0]
        == "Parameter with name 'pipelineParameterName2' and type 'RunParameterType.Pipeline' not found in pipeline 'pipeline'"
    )


def test_when_duplicate_parameters_supplied_should_throw_error() -> None:
    # Arrange
    pipeline = PipelineResource(
        parameters={
            "pipelineParameterName": ParameterSpecification(type=RunParameterType.Pipeline),
            "pipelineParameterName2": ParameterSpecification(type=RunParameterType.Pipeline),
        },
    )
    pipeline.name = "pipeline"

    # Act
    with pytest.raises(ValueError) as exception_info:
        pipeline.validate_parameters(
            [
                RunParameter(RunParameterType.Pipeline, "pipelineParameterName", "pipelineParameterValue"),
                RunParameter(RunParameterType.Pipeline, "pipelineParameterName", "pipelineParameterValue"),
                RunParameter(RunParameterType.Pipeline, "pipelineParameterName2", "pipelineParameterValue2"),
            ],
        )

    # Assert
    assert (
        exception_info.value.args[0]
        == "Duplicate parameter with name 'pipelineParameterName' and type 'RunParameterType.Pipeline' found in pipeline 'pipeline'"
    )
