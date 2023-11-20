from typing import Any, List

from azure_data_factory_testing_framework.models.activities.control_activity import ControlActivity
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameterType
from azure_data_factory_testing_framework.state.run_parameter import RunParameter


class ExecutePipelineActivity(ControlActivity):
    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Execute Pipeline activity in the pipeline.

        Args:
            **kwargs: ExecutePipelineActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "ExecutePipeline"

        super(ControlActivity, self).__init__(**kwargs)

        self.parameters: dict = self.type_properties["parameters"]

    def get_child_run_parameters(self, state: PipelineRunState) -> List[RunParameter]:
        child_parameters = []
        for parameter in state.parameters:
            if parameter.type == RunParameterType.Global:
                child_parameters.append(RunParameter(RunParameterType.Global, parameter.name, parameter.value))

        for parameter_name, parameter_value in self.parameters.items():
            child_parameters.append(RunParameter(RunParameterType.Pipeline, parameter_name, parameter_value.value))

        return child_parameters
