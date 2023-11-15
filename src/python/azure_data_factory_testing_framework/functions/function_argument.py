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
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameterType, RunState


class FunctionArgument:
    def __init__(self, expression: str) -> None:
        """Represents a function argument which can be evaluated into a single value.

        Args:
            expression: The expression of the argument.
        """
        self.expression = expression.strip("\n").strip(" ")

    def evaluate(self, state: RunState) -> str:
        evaluated_expression = find_and_replace_parameters(self.expression, RunParameterType.Pipeline, state)
        evaluated_expression = find_and_replace_parameters(evaluated_expression, RunParameterType.Global, state)
        evaluated_expression = find_and_replace_linked_services(evaluated_expression, state)
        evaluated_expression = find_and_replace_dataset(evaluated_expression, state)
        if isinstance(state, PipelineRunState):
            evaluated_expression = find_and_replace_activity(evaluated_expression, state)
            evaluated_expression = find_and_replace_iteration_item(evaluated_expression, state)
            evaluated_expression = find_and_replace_variables(evaluated_expression, state)
        return _trim_one_char(evaluated_expression, "'")
