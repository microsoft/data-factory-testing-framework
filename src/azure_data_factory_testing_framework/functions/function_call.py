import inspect
from typing import Callable, Union

from azure_data_factory_testing_framework.exceptions.function_call_invalid_arguments_count_error import (
    FunctionCallInvalidArgumentsCountError,
)
from azure_data_factory_testing_framework.exceptions.unsupported_function_error import UnsupportedFunctionError
from azure_data_factory_testing_framework.functions.function_argument import FunctionArgument
from azure_data_factory_testing_framework.functions.functions_repository import FunctionsRepository
from azure_data_factory_testing_framework.state import RunState


class FunctionCall:
    def __init__(self, name: str, arguments: list[Union["FunctionCall", FunctionArgument]]) -> None:
        """Represents a function call with passed arguments that can be evaluated into a single value.

        Args:
            name: The name of the function.
            arguments: The arguments of the function.
        """
        self.name = name
        self.arguments = arguments

    def _validate_function_arguments(
        self, function: Callable, evaluated_arguments: list[Union[str, bool, float, int]]
    ) -> list[Union[str, bool, float, int]]:
        function_signature = inspect.signature(function)
        parameters: list[inspect.Parameter] = list(function_signature.parameters.values())

        # Validate that all arguments are positional or variable length
        if not all(
            [
                param.kind in [inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.VAR_POSITIONAL]
                for param in parameters
            ]
        ):
            raise NotImplementedError("Only positional and variable length arguments are supported.")

        # Validate that the number of arguments is correct
        if all([param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD for param in parameters]) and len(
            evaluated_arguments
        ) != len(parameters):
            raise FunctionCallInvalidArgumentsCountError(
                self.name, evaluated_arguments, function_signature.parameters.keys()
            )

    def evaluate(self, state: RunState) -> str:
        function: Callable = FunctionsRepository.functions.get(self.name)

        if not function:
            raise UnsupportedFunctionError(self.name)

        evaluated_arguments = []
        for argument in self.arguments:
            evaluated_arguments.append(argument.evaluate(state))

        self._validate_function_arguments(function, evaluated_arguments)
        return function(*evaluated_arguments)
