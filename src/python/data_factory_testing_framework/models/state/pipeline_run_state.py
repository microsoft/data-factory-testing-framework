from typing import Any, Dict, List, Optional

from data_factory_testing_framework.exceptions.variable_being_evaluated_does_not_exist_error import (
    VariableBeingEvaluatedDoesNotExistError,
)
from data_factory_testing_framework.exceptions.variable_does_not_exist_error import VariableDoesNotExistError
from data_factory_testing_framework.generated.models import DependencyCondition, VariableSpecification
from data_factory_testing_framework.models.base.pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.state.run_state import RunState


class PipelineRunState(RunState):
    def __init__(self, parameters: Optional[List[RunParameter]] = None, variable_specifications: Optional[Dict[str, VariableSpecification]] = None, pipeline_activity_results: Optional[Dict[str, Any]] = None, iteration_item: str = None):
        if variable_specifications is None:
            variable_specifications = {}

        if pipeline_activity_results is None:
            pipeline_activity_results = {}

        super().__init__(parameters)

        self._variable_specifications = variable_specifications

        self.variables: List[PipelineRunVariable] = []
        for variable_name, variable in variable_specifications.items():
            self.variables.append(PipelineRunVariable(variable_name, variable.default_value))

        self.pipeline_activity_results: Dict[str, Any] = pipeline_activity_results
        self.scoped_pipeline_activity_results: Dict[str, Any] = {}
        self.iteration_item = iteration_item

    def add_activity_result(self, activity_name: str, status: DependencyCondition, output: Any = None):
        self.pipeline_activity_results[activity_name] = {
            "status": status,
            "output": output,
        }
        self.scoped_pipeline_activity_results[activity_name] = {
            "status": status,
            "output": output,
        }

    def create_iteration_scope(self, iteration_item: str):
        return PipelineRunState(self.parameters, self._variable_specifications, self.pipeline_activity_results, iteration_item)

    def add_scoped_activity_results_from_scoped_state(self, scoped_state):
        for result in scoped_state.pipeline_activity_results:
            self.pipeline_activity_results[result] = scoped_state.pipeline_activity_results[result]

    def try_get_scoped_activity_result_by_name(self, name: str):
        return self.pipeline_activity_results[name] if name in self.pipeline_activity_results else None

    def set_variable(self, variable_name: str, value):
        for variable in self.variables:
            if variable.name == variable_name:
                variable.value = value
                return

        raise VariableBeingEvaluatedDoesNotExistError(variable_name)

    def get_variable_by_name(self, variable_name):
        for variable in self.variables:
            if variable.name == variable_name:
                return variable

        raise VariableDoesNotExistError(variable_name)

