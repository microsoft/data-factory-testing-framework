import re

from azure_data_factory_testing_framework.exceptions.variable_not_found_error import VariableNotFoundError
from azure_data_factory_testing_framework.state import PipelineRunState


def find_and_replace_variables(expression: str, state: PipelineRunState) -> str:
    pattern = r"(@?{?variables\(\'(\w+)\'\)}?)"
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        variable_name = match.group(2)
        variable = next((x for x in state.variables if x.name.lower() == variable_name.lower()), None)
        if variable is None:
            raise VariableNotFoundError(variable_name)

        expression = expression.replace(match.group(0), str(variable.value))

    return expression
