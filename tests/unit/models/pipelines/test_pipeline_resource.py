import pytest
from data_factory_testing_framework.models import Pipeline
from data_factory_testing_framework.state import RunParameter, RunParameterType


def test_when_validate_parameters_is_accurate_should_pass() -> None:
    # Arrange
    pipeline = Pipeline(
        pipeline_id="some-id",
        name="pipeline",
        activities=[],
        parameters={
            "pipelineParameterName": {
                "type": "String",
            },
            "pipelineParameterName2": {
                "type": "String",
            },
            "pipelineParameterName3": {
                "type": "String",
                "defaultValue": "pipelineParameterValue3",
            },
        },
    )

    # Act
    parameters = pipeline.validate_and_append_default_parameters(
        [
            RunParameter(RunParameterType.Pipeline, "pipelineParameterName", "pipelineParameterValue"),
            RunParameter(RunParameterType.Pipeline, "pipelineParameterName2", "pipelineParameterValue2"),
        ],
    )

    # Assert
    assert len(parameters) == 3
    assert parameters[0].name == "pipelineParameterName"
    assert parameters[0].value == "pipelineParameterValue"
    assert parameters[1].name == "pipelineParameterName2"
    assert parameters[1].value == "pipelineParameterValue2"
    assert parameters[2].name == "pipelineParameterName3"
    assert parameters[2].value == "pipelineParameterValue3"


@pytest.mark.parametrize(
    ("variable_spec", "expected_value"),
    [
        (
            {
                "type": "String",
                "defaultValue": "stringDefault",
            },
            "stringDefault",
        ),
        (
            {
                "type": "String",
            },
            "",
        ),
        (
            {
                "type": "String",
                "defaultValue": "",
            },
            "",
        ),
        (
            {
                "type": "Boolean",
                "defaultValue": True,
            },
            True,
        ),
        (
            {
                "type": "Boolean",
            },
            False,
        ),
        (
            {
                "type": "Integer",
                "defaultValue": 1,
            },
            1,
        ),
        (
            {
                "type": "Integer",
            },
            0,
        ),
        (
            {
                "type": "Array",
                "defaultValue": ["a", "b"],
            },
            ["a", "b"],
        ),
        (
            {
                "type": "Array",
            },
            [],
        ),
    ],
)
def test_when_get_run_variables_default_values_should_be_used(
    variable_spec: dict[str, str], expected_value: object
) -> None:
    # Arrange
    pipeline = Pipeline(
        pipeline_id="some-id",
        name="pipeline",
        activities=[],
        variables={
            "variable": variable_spec,
        },
    )

    # Act
    variables = pipeline.get_run_variables()

    # Assert
    assert len(variables) == 1
    assert variables[0].name == "variable"
    assert variables[0].value == expected_value


def test_when_validate_parameters_is_missing_run_parameter_should_throw_error() -> None:
    # Arrange
    pipeline = Pipeline(
        pipeline_id="some-id",
        name="pipeline",
        activities=[],
        parameters={
            "pipelineParameterName": {
                "type": "String",
            },
            "pipelineParameterName2": {
                "type": "String",
            },
        },
    )
    pipeline.name = "pipeline"

    # Act
    with pytest.raises(ValueError) as exception_info:
        pipeline.validate_and_append_default_parameters(
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
    pipeline = Pipeline(
        pipeline_id="some-id",
        name="pipeline",
        activities=[],
        parameters={
            "pipelineParameterName": {
                "type": "String",
            },
            "pipelineParameterName2": {
                "type": "String",
            },
        },
    )
    pipeline.name = "pipeline"

    # Act
    with pytest.raises(ValueError) as exception_info:
        pipeline.validate_and_append_default_parameters(
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
