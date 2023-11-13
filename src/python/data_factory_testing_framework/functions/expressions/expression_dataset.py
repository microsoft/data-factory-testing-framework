import re

from data_factory_testing_framework.exceptions.dataset_parameter_not_found_error import DatasetParameterNotFoundError
from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def find_and_replace_dataset(expression: str, state: PipelineRunState):
    pattern = r'(@?{?dataset\(\'(\w+)\'\)}?)'
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        data_set_name = match.group(2)
        data_set = next((x for x in state.parameters if x.name.lower() == data_set_name.lower() and x.type == RunParameterType.Dataset), None)
        if data_set is None:
            raise DatasetParameterNotFoundError(data_set_name)

        expression = expression.replace(match.group(0), str(data_set.value))

    return expression
