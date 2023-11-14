from typing import List

from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


class ExecutePipelineActivity:
    @staticmethod
    def get_child_run_parameters(state: PipelineRunState) -> List[RunParameter]:
        child_parameters = []
        for parameter in state.parameters:
            if parameter.type == RunParameterType.Global:
                child_parameters.append(RunParameter(RunParameterType.Global, parameter.name, parameter.value))

        return child_parameters
