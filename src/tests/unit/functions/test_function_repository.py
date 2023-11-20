from unittest.mock import Mock

from azure_data_factory_testing_framework.functions.functions_repository import FunctionsRepository


def test_function_registration() -> None:
    # Arrange
    function_spy = Mock()

    # Act
    FunctionsRepository.register("function_name", function_spy)

    # Assert
    assert FunctionsRepository.functions["function_name"] == function_spy
