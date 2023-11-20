import re
from typing import Union

from azure_data_factory_testing_framework.exceptions.variable_not_found_error import VariableNotFoundError
from azure_data_factory_testing_framework.state import PipelineRunState


def find_and_replace_variables(expression: str, state: PipelineRunState) -> (Union[str, bool, int, float], bool):
    pattern = r"(@?{?variables\(\'(\w+)\'\)}?)"
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        variable_name = match.group(2)
        variable = next((x for x in state.variables if x.name.lower() == variable_name.lower()), None)
        if variable is None:
            raise VariableNotFoundError(variable_name)

        if expression == match.group(0):
            return variable.value, True

        expression = expression.replace(match.group(0), str(variable.value))

    return expression, False
