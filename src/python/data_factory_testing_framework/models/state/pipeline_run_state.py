from typing import List, Dict

from data_factory_testing_framework.generated.models import VariableSpecification
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.base.run_variable import RunVariable
from data_factory_testing_framework.models.state.run_state import RunState


class PipelineRunState(RunState):
    def __init__(self, parameters: List[RunParameter] = [], variables: Dict[str, VariableSpecification] = []):
        super().__init__(parameters)
        self.variables = []
        for variable in variables:
            self.variables.append(RunVariable(variable.name, variable.default_value))

        self.pipeline_activity_results = []
        self.scoped_pipeline_activity_results = []
        self.iteration_item = None

    def add_activity_result(self, activity):
        self.pipeline_activity_results.append(activity)
        self.scoped_pipeline_activity_results.append(activity)
