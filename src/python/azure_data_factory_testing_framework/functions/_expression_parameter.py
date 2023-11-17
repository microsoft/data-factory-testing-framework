import re
from typing import Union

from azure_data_factory_testing_framework.exceptions.expression_parameter_not_found_error import (
    ExpressionParameterNotFoundError,
)
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameterType


def find_and_replace_parameters(
    expression: str, parameter_type: RunParameterType, state: PipelineRunState
) -> (Union[str, bool, int, float], bool):
    pattern = rf"(@?{{?pipeline\(\)\.{_get_parameter_string_template(parameter_type)}\.(\w+)}}?)"
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        parameter_name = match.group(2)
        parameter = next(
            (x for x in state.parameters if x.name.lower() == parameter_name.lower() and x.type == parameter_type),
            None,
        )
        if parameter is None:
            raise ExpressionParameterNotFoundError(parameter_name)

        if expression == match.group(0):
            return parameter.value, True

        expression = expression.replace(match.group(0), str(parameter.value))

    return expression, False


def _get_parameter_string_template(parameter_type: RunParameterType) -> str:
    if parameter_type == RunParameterType.Pipeline:
        return "parameters"
    elif parameter_type == RunParameterType.Global:
        return "globalParameters"
    else:
        raise ValueError(f"Parameter type not supported: {parameter_type}")
