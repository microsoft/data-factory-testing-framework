from typing import Any, List

from azure_data_factory_testing_framework.exceptions.activity_not_found_error import ActivityNotFoundError
from azure_data_factory_testing_framework.models.activities.activity import Activity
from azure_data_factory_testing_framework.state import PipelineRunVariable, RunParameter, RunParameterType


class Pipeline:
    def __init__(
        self,
        name: str,
        activities: List[Activity],
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """This is the class that represents a pipeline.

        Args:
            name: Name of the pipeline.
            activities: List of activities in the pipeline.
            **kwargs: Pipeline properties coming directly from the json representation of the pipeline.
        """
        self.name = name
        self.parameters: dict = kwargs["parameters"] if "parameters" in kwargs else {}
        self.variables: dict = kwargs["variables"] if "variables" in kwargs else {}
        self.activities = activities
        self.annotations = kwargs["annotations"] if "annotations" in kwargs else []

    def get_activity_by_name(self, name: str) -> Activity:
        """Get an activity by name. Throws an exception if the activity is not found.

        Args:
            name: Name of the activity.
        """
        for activity in self.activities:
            if activity.name == name:
                return activity

        raise ActivityNotFoundError(f"Activity with name {name} not found")

    def validate_parameters(self, parameters: List[RunParameter]) -> None:
        """Validate that all parameters are provided and that no duplicate parameters are provided.

        Args:
            parameters: List of parameters.
        """
        # Check if all parameters are provided
        for pipeline_parameter_name, _ in self.parameters.items():
            found = False
            for parameter in parameters:
                if pipeline_parameter_name == parameter.name and parameter.type == RunParameterType.Pipeline:
                    found = True
                    break

            if not found:
                raise ValueError(
                    f"Parameter with name '{pipeline_parameter_name}' and type 'RunParameterType.Pipeline' not found in pipeline '{self.name}'",
                )

        # Check if no duplicate parameters are provided
        for parameter in parameters:
            if sum(1 for p in parameters if p.name == parameter.name and p.type == parameter.type) > 1:
                raise ValueError(
                    f"Duplicate parameter with name '{parameter.name}' and type '{parameter.type}' found in pipeline '{self.name}'",
                )

    def get_run_variables(self) -> List[PipelineRunVariable]:
        """Get the run variables for the pipeline. This can be used to generate the instance variables for a pipeline run."""
        run_variables = []
        for variable_name, variable_value in self.variables.items():
            run_variables.append(PipelineRunVariable(variable_name, variable_value.get("default_value", None)))

        return run_variables
