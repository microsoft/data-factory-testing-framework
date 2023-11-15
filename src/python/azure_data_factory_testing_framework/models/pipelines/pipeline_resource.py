from typing import List

from azure_data_factory_testing_framework.exceptions.activity_not_found_error import ActivityNotFoundError
from azure_data_factory_testing_framework.generated.models import Activity, PipelineResource
from azure_data_factory_testing_framework.state import RunParameterType
from azure_data_factory_testing_framework.state.run_parameter import RunParameter


class PipelineResource:
    def get_activity_by_name(self: PipelineResource, name: str) -> Activity:
        """Get an activity by name. Throws an exception if the activity is not found.

        Args:
            name: Name of the activity.
        """
        for activity in self.activities:
            if activity.name == name:
                return activity

        raise ActivityNotFoundError(f"Activity with name {name} not found")

    def validate_parameters(self: PipelineResource, parameters: List[RunParameter]) -> None:
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
                    f"Duplicate parameter with name '{parameter.name}' and type 'RunParameterType.{parameter.type}' found in pipeline '{self.name}'",
                )
