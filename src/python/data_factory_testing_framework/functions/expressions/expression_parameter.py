import re

from data_factory_testing_framework.exceptions.expression_parameter_not_found_error import (
    ExpressionParameterNotFoundError,
)
from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def find_and_replace_parameters(expression: str, parameter_type: RunParameterType, state: PipelineRunState):
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

        expression = expression.replace(match.group(0), str(parameter.value))

    return expression


def _get_parameter_string_template(parameter_type: RunParameterType):
    if parameter_type == RunParameterType.Pipeline:
        return "parameters"
    elif parameter_type == RunParameterType.Global:
        return "globalParameters"
    else:
        raise ValueError(f"Parameter type not supported: {parameter_type}")
