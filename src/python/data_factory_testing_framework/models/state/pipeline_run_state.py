from typing import List, Dict

from data_factory_testing_framework.exceptions.variable_being_evaluated_does_not_exist_error import \
    VariableBeingEvaluatedDoesNotExistError
from data_factory_testing_framework.generated.models import VariableSpecification
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.base.pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.models.state.run_state import RunState


class PipelineRunState(RunState):
    def __init__(self, parameters: List[RunParameter] = [], variables: Dict[str, VariableSpecification] = [], pipeline_activity_results: List[RunState] = [], iteration_item: str = None):
        super().__init__(parameters)
        self.variables = []
        for variable in variables:
            self.variables.append(PipelineRunVariable(variable.name, variable.value))

        self.pipeline_activity_results = pipeline_activity_results
        self.scoped_pipeline_activity_results = []
        self.iteration_item = iteration_item

    def add_activity_result(self, activity):
        self.pipeline_activity_results.append(activity)
        self.scoped_pipeline_activity_results.append(activity)

    def create_iteration_scope(self, iteration_item: str):
        return PipelineRunState(self.parameters, self.variables, self.pipeline_activity_results, iteration_item)

    def add_scoped_activity_results_from_scoped_state(self, scoped_state):
        self.pipeline_activity_results.extend(scoped_state.pipeline_activity_results)

    def set_variable(self, variable_name: str, value):
        for variable in self.variables:
            if variable.name == variable_name:
                variable.value = value
                return

        raise VariableBeingEvaluatedDoesNotExistError(variable_name)
