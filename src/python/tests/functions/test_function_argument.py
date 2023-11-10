import pytest

from data_factory_testing_framework.exceptions.dataset_parameter_not_found_error import DatasetParameterNotFoundError
from data_factory_testing_framework.exceptions.expression_parameter_not_found_error import \
    ExpressionParameterNotFoundError
from data_factory_testing_framework.exceptions.linked_service_parameter_not_found_error import \
    LinkedServiceParameterNotFoundError
from data_factory_testing_framework.exceptions.variable_not_found_error import VariableNotFoundError
from data_factory_testing_framework.functions.function_argument import FunctionArgument
from data_factory_testing_framework.models.base.pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def test_evaluate_parameter_expression():
    # Arrange
    expression = "pipeline().parameters.parameterName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.Pipeline, "parameterName", "parameterValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "parameterValue"


def test_evaluate_global_parameter_expression():
    # Arrange
    expression = "pipeline().globalParameters.parameterName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.Global, "parameterName", "parameterValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "parameterValue"


def test_evaluate_variable_string_expression():
    # Arrange
    expression = "variables('variableName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.variables.append(PipelineRunVariable("variableName", "variableValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "variableValue"


def test_evaluate_linked_service_string_expression():
    # Arrange
    expression = "linkedService('linkedServiceName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.LinkedService, "linkedServiceName", "linkedServiceNameValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "linkedServiceNameValue"


def test_evaluate_dataset_string_expression():
    # Arrange
    expression = "dataset('datasetName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.parameters.append(RunParameter(RunParameterType.Dataset, "datasetName", "datasetNameValue"))

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "datasetNameValue"


def test_evaluate_iteration_item_string_expression():
    # Arrange
    expression = "item()"
    argument = FunctionArgument(expression)
    state = PipelineRunState()
    state.iteration_item = "iterationItemValue"

    # Act
    evaluated = argument.evaluate(state)

    # Assert
    assert evaluated == "iterationItemValue"


def test_evaluate_unknown_pipeline_parameter():
    # Arrange
    expression = "pipeline().parameters.parameterName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(ExpressionParameterNotFoundError):
        argument.evaluate(state)


def test_evaluate_unknown_global_pipeline_parameter():
    # Arrange
    expression = "pipeline().globalParameters.parameterName"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(ExpressionParameterNotFoundError):
        argument.evaluate(state)


def test_evaluate_unknown_variable():
    # Arrange
    expression = "variables('variableName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(VariableNotFoundError):
        argument.evaluate(state)


def test_evaluate_unknown_dataset():
    # Arrange
    expression = "dataset('datasetName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(DatasetParameterNotFoundError):
        argument.evaluate(state)


def test_evaluate_unknown_linked_service():
    # Arrange
    expression = "linkedService('linkedServiceName')"
    argument = FunctionArgument(expression)
    state = PipelineRunState()

    # Act
    with pytest.raises(LinkedServiceParameterNotFoundError):
        argument.evaluate(state)



