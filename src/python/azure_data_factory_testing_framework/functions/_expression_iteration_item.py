import re

from azure_data_factory_testing_framework.exceptions.state_iteration_item_not_set_error import (
    StateIterationItemNotSetError,
)
from azure_data_factory_testing_framework.state import PipelineRunState


def find_and_replace_iteration_item(expression: str, state: PipelineRunState) -> str:
    pattern = r"(@?{?item\(\)\}?)"
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        if state.iteration_item is None:
            raise StateIterationItemNotSetError()

        expression = expression.replace(match.group(0), state.iteration_item)

    return expression
