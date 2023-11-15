from typing import List

from azure_data_factory_testing_framework.generated.models import ExecutePipelineActivity
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameterType
from azure_data_factory_testing_framework.state.run_parameter import RunParameter


class ExecutePipelineActivity:

    def get_child_run_parameters(self: ExecutePipelineActivity, state: PipelineRunState) -> List[RunParameter]:
        child_parameters = []
        for parameter in state.parameters:
            if parameter.type == RunParameterType.Global:
                child_parameters.append(RunParameter(RunParameterType.Global, parameter.name, parameter.value))

        for parameter_name, parameter_value in self.parameters.items():
            child_parameters.append(RunParameter(RunParameterType.Pipeline, parameter_name, parameter_value.value))

        return child_parameters
