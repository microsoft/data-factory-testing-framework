import re
from typing import Union

from azure_data_factory_testing_framework.exceptions.linked_service_parameter_not_found_error import (
    LinkedServiceParameterNotFoundError,
)
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameterType


def find_and_replace_linked_services(expression: str, state: PipelineRunState) -> (Union[str, bool, int, float], bool):
    pattern = r"(@?{?linkedService\(\'(\w+)\'\)}?)"
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        linked_service_name = match.group(2)
        linked_service = next(
            (
                x
                for x in state.parameters
                if x.name.lower() == linked_service_name.lower() and x.type == RunParameterType.LinkedService
            ),
            None,
        )
        if linked_service is None:
            raise LinkedServiceParameterNotFoundError(linked_service_name)

        if expression == match.group(0):
            return linked_service.value, True

        expression = expression.replace(match.group(0), str(linked_service.value))

    return expression, False
