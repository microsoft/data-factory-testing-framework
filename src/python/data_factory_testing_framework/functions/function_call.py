import inspect
from typing import List

from data_factory_testing_framework.exceptions.unsupported_function_error import UnsupportedFunctionError
from data_factory_testing_framework.functions.functions_repository import FunctionsRepository


class FunctionCall:
    def __init__(self, name: str, arguments: List):
        self.name = name
        self.arguments = arguments

    def evaluate(self, state):
        function = FunctionsRepository.functions.get(self.name)
        if not function:
            raise UnsupportedFunctionError(self.name)

        evaluated_arguments = []
        for argument in self.arguments:
            evaluated_arguments.append(argument.evaluate(state))

        signature = inspect.signature(function)
        parameters = signature.parameters
        if len(parameters) == 1:
            return function(evaluated_arguments)

        return function(*evaluated_arguments)
