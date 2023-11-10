from typing import List

from data_factory_testing_framework.functions.function_argument import FunctionArgument


class FunctionCall:
    def __init__(self, name: str, arguments: List):
        self.name = name
        self.arguments = arguments
