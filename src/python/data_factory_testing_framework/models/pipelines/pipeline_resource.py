from typing import List

from data_factory_testing_framework.exceptions.activity_not_found_exception import ActivityNotFoundException
from data_factory_testing_framework.generated.models import PipelineResource, Activity
from data_factory_testing_framework.models.base.run_parameter import RunParameter


class PipelineResource:
    def get_activity_by_name(self: PipelineResource, name: str) -> Activity:
        for activity in self.activities:
            if activity.name == name:
                return activity

        raise ActivityNotFoundException(f"Activity with name {name} not found")

    def validate_parameters(self: PipelineResource, parameters: List[RunParameter]):
        # Check if all parameters are provided
        for pipeline_parameter_name, pipeline_parameter_specification in self.parameters.items():
            found = False
            for parameter in parameters:
                if pipeline_parameter_name == parameter.name and pipeline_parameter_specification.type == parameter.type:
                    found = True
                    break

            if not found:
                raise ValueError(f"Parameter with name '{pipeline_parameter_name}' and type '{pipeline_parameter_specification.type}' not found in pipeline '{self.name}'")

        # Check if no duplicate parameters are provided
        for parameter in parameters:
            if sum(1 for p in parameters if p.name == parameter.name and p.type == parameter.type) > 1:
                raise ValueError(f"Duplicate parameter with name '{parameter.name}' and type '{parameter.type}' found in pipeline '{self.name}'")
