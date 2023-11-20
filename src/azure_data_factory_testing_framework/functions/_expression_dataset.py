import re
from typing import Union

from azure_data_factory_testing_framework.exceptions.dataset_parameter_not_found_error import (
    DatasetParameterNotFoundError,
)
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameterType


def find_and_replace_dataset(expression: str, state: PipelineRunState) -> (Union[str, bool, int, float], bool):
    pattern = r"(@?{?dataset\(\'(\w+)\'\)}?)"
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        data_set_name = match.group(2)
        data_set = next(
            (
                x
                for x in state.parameters
                if x.name.lower() == data_set_name.lower() and x.type == RunParameterType.Dataset
            ),
            None,
        )
        if data_set is None:
            raise DatasetParameterNotFoundError(data_set_name)

        if expression == match.group(0):
            return data_set.value, True

        expression = expression.replace(match.group(0), str(data_set.value))

    return expression, False
