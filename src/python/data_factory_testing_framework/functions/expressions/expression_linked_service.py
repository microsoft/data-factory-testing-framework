import re

from data_factory_testing_framework.exceptions.linked_service_parameter_not_found_error import (
    LinkedServiceParameterNotFoundError,
)
from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def find_and_replace_linked_services(expression: str, state: PipelineRunState) -> str:
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

        expression = expression.replace(match.group(0), str(linked_service.value))

    return expression
