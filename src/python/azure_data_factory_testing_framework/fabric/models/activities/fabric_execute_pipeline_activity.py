from typing import Any, List

from azure_data_factory_testing_framework.fabric.models.activities.fabric_control_activity import FabricControlActivity
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameterType
from azure_data_factory_testing_framework.state.run_parameter import RunParameter


class FabricExecutePipelineActivity(FabricControlActivity):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Execute Pipeline activity in the pipeline."""
        super(FabricControlActivity, self).__init__(*args, **kwargs)

    def get_child_run_parameters(self, state: PipelineRunState) -> List[RunParameter]:
        child_parameters = []
        for parameter in state.parameters:
            if parameter.type == RunParameterType.Global:
                child_parameters.append(RunParameter(RunParameterType.Global, parameter.name, parameter.value))

        for parameter_name, parameter_value in self.parameters.items():
            child_parameters.append(RunParameter(RunParameterType.Pipeline, parameter_name, parameter_value.value))

        return child_parameters
