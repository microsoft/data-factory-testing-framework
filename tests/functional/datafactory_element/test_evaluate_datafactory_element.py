import pytest
from data_factory_testing_framework.exceptions import (
    DataFactoryElementEvaluationError,
    ParameterNotFoundError,
)
from data_factory_testing_framework.exceptions._user_error import UserError
from data_factory_testing_framework.models import DataFactoryElement
from data_factory_testing_framework.state import PipelineRunState


def test_evaluate_datafactory_element() -> None:
    # Arrange
    expression = "@mul(2, 3)"
    state = PipelineRunState()
    data_factory_element = DataFactoryElement(expression)

    # Act
    result = data_factory_element.evaluate(state)

    # Assert
    assert result == 6


def test_evaluate_datafactory_element_passes_user_error_through() -> None:
    # Arrange
    expression = "@pipeline().parameters.pipelineName"
    state = PipelineRunState()
    data_factory_element = DataFactoryElement(expression)

    # Act
    with pytest.raises(UserError) as e:
        data_factory_element.evaluate(state)

    # Assert
    assert isinstance(e.value, ParameterNotFoundError)


def test_evaluate_datafactory_element_raises_technical_errors() -> None:
    # Arrange
    expression = "@FAULTY_EXPRESSION()"
    state = PipelineRunState()
    data_factory_element = DataFactoryElement(expression)

    # Act
    with pytest.raises(DataFactoryElementEvaluationError):
        data_factory_element.evaluate(state)
