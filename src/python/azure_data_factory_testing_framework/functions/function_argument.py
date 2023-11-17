from typing import Union

from azure_data_factory_testing_framework.functions._expression_activity import find_and_replace_activity
from azure_data_factory_testing_framework.functions._expression_dataset import find_and_replace_dataset
from azure_data_factory_testing_framework.functions._expression_iteration_item import (
    find_and_replace_iteration_item,
)
from azure_data_factory_testing_framework.functions._expression_linked_service import (
    find_and_replace_linked_services,
)
from azure_data_factory_testing_framework.functions._expression_parameter import find_and_replace_parameters
from azure_data_factory_testing_framework.functions._expression_variable import find_and_replace_variables
from azure_data_factory_testing_framework.functions._string_utils import _trim_one_char
from azure_data_factory_testing_framework.state import RunParameterType, RunState

replace_functions = [
    lambda expression, state: find_and_replace_parameters(expression, RunParameterType.Pipeline, state),
    lambda expression, state: find_and_replace_parameters(expression, RunParameterType.Global, state),
    lambda expression, state: find_and_replace_linked_services(expression, state),
    lambda expression, state: find_and_replace_dataset(expression, state),
    lambda expression, state: find_and_replace_activity(expression, state),
    lambda expression, state: find_and_replace_iteration_item(expression, state),
    lambda expression, state: find_and_replace_variables(expression, state),
]


class FunctionArgument:
    def __init__(self, expression: str) -> None:
        """Represents a function argument which can be evaluated into a single value.

        Args:
            expression: The expression of the argument.
        """
        self.expression = expression.strip("\n").strip(" ")

    def evaluate(self, state: RunState) -> Union[str, int, bool, float]:
        evaluated_expression = self.expression
        for replace_function in replace_functions:
            evaluated_expression, full_match_bool = replace_function(evaluated_expression, state)
            if full_match_bool:
                return evaluated_expression

        if evaluated_expression.lower() == "true" or evaluated_expression.lower() == "false":
            return evaluated_expression.lower() == "true"
        elif evaluated_expression.lstrip("-").isdigit():
            return int(evaluated_expression)
        elif evaluated_expression.replace(".", "", 1).isdigit():
            return float(evaluated_expression)

        return _trim_one_char(evaluated_expression, "'")
