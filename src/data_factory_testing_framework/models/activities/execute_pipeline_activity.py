from typing import Any, Callable, Iterator, List

from data_factory_testing_framework.models.activities.activity import Activity
from data_factory_testing_framework.models.activities.control_activity import ControlActivity
from data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.pipeline import Pipeline
from data_factory_testing_framework.state import PipelineRunState, RunParameterType
from data_factory_testing_framework.state.run_parameter import RunParameter


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
            if parameter.type == RunParameterType.Global or parameter.type == RunParameterType.System:
                child_parameters.append(RunParameter(parameter.type, parameter.name, parameter.value))

        for parameter_name, parameter_value in self.parameters.items():
            parameter_value = (
                parameter_value.value if isinstance(parameter_value, DataFactoryElement) else parameter_value
            )
            child_parameters.append(RunParameter(RunParameterType.Pipeline, parameter_name, parameter_value))

        return child_parameters

    def evaluate_pipeline(
        self,
        pipeline: Pipeline,
        parameters: List[RunParameter],
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
    ) -> Iterator[Activity]:
        parameters = pipeline.validate_and_append_default_parameters(parameters)
        scoped_state = PipelineRunState(parameters, pipeline.get_run_variables())
        for activity in evaluate_activities(pipeline.activities, scoped_state):
            yield activity

        # Set the pipelineReturnValues as evaluated by SetVariable activities to the ExecutePipelineActivity output
        self.output["pipelineReturnValue"] = {}
        for key in scoped_state.return_values:
            self.output["pipelineReturnValue"][key] = scoped_state.return_values[key]
