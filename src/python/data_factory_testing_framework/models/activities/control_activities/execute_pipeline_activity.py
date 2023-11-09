from typing import List

from data_factory_testing_framework.generated.models import ExecutePipelineActivity
from data_factory_testing_framework.models.base.parameter_type import ParameterType
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


class ExecutePipelineActivity:

    def get_child_run_parameters(self, state: PipelineRunState) -> List[RunParameter]:
        child_parameters = []
        for parameter in state.parameters:
            if parameter.type == ParameterType.Global:
                child_parameters.append(RunParameter(ParameterType.Global, parameter.name, parameter.value))

        return child_parameters
