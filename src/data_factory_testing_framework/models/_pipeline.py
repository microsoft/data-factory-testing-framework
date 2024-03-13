from typing import TYPE_CHECKING, Any, List

from data_factory_testing_framework.exceptions import ActivityNotFoundError

if TYPE_CHECKING:
    from data_factory_testing_framework.models.activities._activity import Activity
from data_factory_testing_framework.state import PipelineRunVariable, RunParameter, RunParameterType


class Pipeline:
    def __init__(
        self,
        pipeline_id: str,
        name: str,
        activities: List["Activity"],
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """This is the class that represents a pipeline.

        Args:
            pipeline_id: Identifier of the pipeline.
            name: Name of the pipeline.
            activities: List of activities in the pipeline.
            **kwargs: Pipeline properties coming directly from the json representation of the pipeline.
        """
        self.pipeline_id = pipeline_id
        self.name = name
        self.parameters: dict = kwargs["parameters"] if "parameters" in kwargs else {}
        self.variables: dict = kwargs["variables"] if "variables" in kwargs else {}
        self.activities = activities
        self.annotations = kwargs["annotations"] if "annotations" in kwargs else []

    def get_activity_by_name(self, name: str) -> "Activity":
        """Get an activity by name. Throws an exception if the activity is not found.

        Args:
            name: Name of the activity.
        """
        for activity in self.activities:
            if activity.name == name:
                return activity

        raise ActivityNotFoundError(f"Activity with name {name} not found")

    def validate_and_append_default_parameters(self, parameters: List[RunParameter]) -> List[RunParameter]:
        """Validate that all parameters are provided and that no duplicate parameters are provided.

        Args:
            parameters: List of parameters.
        """
        # Check if all parameters are provided
        run_parameters = parameters
        for pipeline_parameter_name, pipeline_parameter in self.parameters.items():
            found = False
            for parameter in parameters:
                if pipeline_parameter_name == parameter.name and parameter.type == RunParameterType.Pipeline:
                    found = True
                    break

            if not found:
                if "defaultValue" in pipeline_parameter:
                    run_parameters.append(
                        RunParameter(
                            RunParameterType.Pipeline, pipeline_parameter_name, pipeline_parameter["defaultValue"]
                        )
                    )
                    continue

                raise ValueError(
                    f"Parameter with name '{pipeline_parameter_name}' and type 'RunParameterType.Pipeline' not found in pipeline '{self.name}'",
                )

        # Check if no duplicate parameters are provided
        for parameter in parameters:
            if sum(1 for p in parameters if p.name == parameter.name and p.type == parameter.type) > 1:
                raise ValueError(
                    f"Duplicate parameter with name '{parameter.name}' and type '{parameter.type}' found in pipeline '{self.name}'",
                )

        return parameters

    def get_run_variables(self) -> List[PipelineRunVariable]:
        """Get the run variables for the pipeline. This can be used to generate the instance variables for a pipeline run."""
        run_variables = []
        for variable_name, variable_value in self.variables.items():
            run_variables.append(PipelineRunVariable(variable_name, variable_value.get("default_value", None)))

        return run_variables
