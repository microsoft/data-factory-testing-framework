from unittest.mock import patch

import pytest
from data_factory_testing_framework._expression_runtime.expression_runtime import ExpressionRuntime
from data_factory_testing_framework.exceptions import (
    DataFactoryElementEvaluationError,
    ParameterNotFoundError,
)
from data_factory_testing_framework.exceptions._user_error import UserError
from data_factory_testing_framework.models import DataFactoryElement, _data_factory_element
from data_factory_testing_framework.models._data_factory_element import _get_expression_runtime
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


def test_evaluate_datafactory_element_reuses_one_expression_runtime() -> None:
    # Arrange
    _get_expression_runtime.cache_clear()
    state = PipelineRunState()
    elements = [DataFactoryElement("@mul(2, 3)"), DataFactoryElement("@add(2, 3)")]

    # Act
    with patch.object(_data_factory_element, "ExpressionRuntime", wraps=ExpressionRuntime) as runtime_class:
        results = [element.evaluate(state) for element in elements]
        results.append(elements[0].evaluate(state))

    # Assert
    assert results == [6, 5, 6]
    assert runtime_class.call_count == 1
