import pytest

from data_factory_testing_framework.exceptions.dataset_parameter_not_found_error import DatasetParameterNotFoundError
from data_factory_testing_framework.exceptions.expression_parameter_not_found_error import (
    ExpressionParameterNotFoundError,
)
from data_factory_testing_framework.exceptions.linked_service_parameter_not_found_error import (
    LinkedServiceParameterNotFoundError,
)
from data_factory_testing_framework.exceptions.variable_not_found_error import VariableNotFoundError
from data_factory_testing_framework.functions.function_argument import FunctionArgument
from data_factory_testing_framework.generated.models import DependencyCondition, VariableSpecification
from data_factory_testing_framework.state import PipelineRunState, RunParameterType
from data_factory_testing_framework.state.run_parameter import RunParameter


def test_evaluate_parameter_expression() -> None:
    # Arrange
    expression = "pipeline().parameters.parameterName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.Pipeline, "parameterName", "parameterValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "parameterValue"


def test_evaluate_global_parameter_expression() -> None:
    # Arrange
    expression = "pipeline().globalParameters.parameterName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.Global, "parameterName", "parameterValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "parameterValue"


def test_evaluate_variable_string_expression() -> None:
    # Arrange
    expression = "variables('variableName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState(
        variable_specifications={
            "variableName": VariableSpecification(type="String", default_value="variableValue"),
        },
    )

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "variableValue"


def test_evaluate_linked_service_string_expression() -> None:
    # Arrange
    expression = "@linkedService('linkedServiceName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.LinkedService, "linkedServiceName", "linkedServiceNameValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "linkedServiceNameValue"


def test_evaluate_dataset_string_expression() -> None:
    # Arrange
    expression = "dataset('datasetName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.Dataset, "datasetName", "datasetNameValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "datasetNameValue"


def test_evaluate_iteration_item_string_expression() -> None:
    # Arrange
    expression = "item()"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.iteration_item = "iterationItemValue"

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "iterationItemValue"


def test_evaluate_unknown_pipeline_parameter() -> None:
    # Arrange
    expression = "pipeline().parameters.parameterName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(ExpressionParameterNotFoundError):
        argument.evaluate(state)
        print("hi")


def test_evaluate_unknown_global_pipeline_parameter() -> None:
    # Arrange
    expression = "pipeline().globalParameters.parameterName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(ExpressionParameterNotFoundError):
        argument.evaluate(state)


def test_evaluate_unknown_variable() -> None:
    # Arrange
    expression = "variables('variableName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(VariableNotFoundError):
        argument.evaluate(state)


def test_evaluate_unknown_dataset() -> None:
    # Arrange
    expression = "dataset('datasetName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(DatasetParameterNotFoundError):
        argument.evaluate(state)


def test_evaluate_unknown_linked_service() -> None:
    # Arrange
    expression = "linkedService('linkedServiceName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(LinkedServiceParameterNotFoundError):
        argument.evaluate(state)


def test_evaluate_activity_output_expression() -> None:
    # Arrange
    expression = "activity('activityName').output.outputName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.add_activity_result("activityName", DependencyCondition.SUCCEEDED, {"outputName": "outputValue"})

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "outputValue"


def test_evaluate_activity_output_nested_expression() -> None:
    # Arrange
    expression = "activity('activityName').output.nestedOutput.nestedField"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.add_activity_result(
        "activityName",
        DependencyCondition.SUCCEEDED,
        {"nestedOutput": {"nestedField": "outputValue"}},
    )

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "outputValue"


def test_evaluate_complex_json_expression() -> None:
    # Arrange
    expression = (
        '" { "command": "@pipeline().globalParameters.command", "argument": @pipeline().parameters.argument } "'
    )
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.Global, "command", "commandValue"))
    state.parameters.append(RunParameter(RunParameterType.Pipeline, "argument", "argumentValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == '" { "command": "commandValue", "argument": argumentValue } "'
