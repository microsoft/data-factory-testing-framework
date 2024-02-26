import inspect
import types
from typing import Callable

from tests.functional import utils


def test_functions_repository_api() -> None:
    # Arrange
    from data_factory_testing_framework import FunctionsRepository

    # Act
    public_attributes = [attribute for attribute in dir(FunctionsRepository) if not attribute.startswith("_")]

    # Assert
    assert public_attributes == ["register"]


def test_functions_repository_method_types() -> None:
    # Arrange
    from data_factory_testing_framework import FunctionsRepository

    # Act
    method_types = {
        name: type(getattr(FunctionsRepository, name)) for name in dir(FunctionsRepository) if not name.startswith("_")
    }

    # Assert
    assert method_types == {
        "register": types.FunctionType,
    }


def test_functions_repository_method_signatures() -> None:
    # Arrange
    from data_factory_testing_framework import FunctionsRepository

    methods = [method[0] for method in inspect.getmembers(FunctionsRepository, predicate=utils.is_public_method)]

    # Act
    method_signatures = {name: inspect.signature(getattr(FunctionsRepository, name)) for name in methods}

    # Assert
    assert method_signatures == {
        "register": inspect.Signature(
            parameters=[
                inspect.Parameter(
                    name="function_name",
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=str,
                ),
                inspect.Parameter(
                    name="function",
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Callable,
                ),
            ],
            return_annotation=None,
        ),
    }
