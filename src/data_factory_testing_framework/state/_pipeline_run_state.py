from typing import Any, Dict, List, Optional

from data_factory_testing_framework.exceptions import (
    ActivityNotFoundError,
    ParameterNotFoundError,
    VariableBeingEvaluatedDoesNotExistError,
    VariableNotFoundError,
)
from data_factory_testing_framework.models._data_factory_object_type import DataFactoryObjectType
from data_factory_testing_framework.state._activity_result import ActivityResult
from data_factory_testing_framework.state._dependency_condition import DependencyCondition
from data_factory_testing_framework.state._pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.state._run_parameter import RunParameter
from data_factory_testing_framework.state._run_parameter_type import RunParameterType
from data_factory_testing_framework.state._run_state import RunState


class PipelineRunState(RunState):
    def __init__(
        self,
        parameters: Optional[List[RunParameter]] = None,
        variables: Optional[List[PipelineRunVariable]] = None,
        activity_results: Optional[List[ActivityResult]] = None,
        iteration_item: Optional[Any] = None,  # noqa: ANN401
    ) -> None:
        """Represents the state of a pipeline run. Can be used to configure the state to validate certain pipeline conditions.

        Args:
            parameters: The global and regular parameters to be used for evaluating expressions.
            variables: The initial variables specification to use for the pipeline run.
            activity_results: The results of previous activities to use for validating dependencyConditions and evaluating expressions
            (i.e. activity('activityName').output).
            iteration_item: The current item() of a ForEach activity.
        """
        if variables is None:
            variables = []

        if activity_results is None:
            activity_results = []

        super().__init__(parameters)

        self.variables = variables
        self.activity_results: List[ActivityResult] = activity_results
        self.scoped_activity_results: List[ActivityResult] = []
        self.iteration_item = iteration_item
        self.return_values: Dict[str, Any] = {}

    def add_activity_result(
        self,
        activity_name: str,
        status: DependencyCondition,
        output: Optional[Any] = None,  # noqa: ANN401
    ) -> None:  # noqa: ANN401
        """Registers the result of an activity to the pipeline run state.

        Args:
            activity_name: Name of the activity.
            status: Status of the activity.
            output: Output of the activity. (e.g. { "count": 1 } for activity('activityName').output.count)
        """
        self.activity_results = self._update_activity_result_in_collection(
            self.activity_results, activity_name, status, output
        )
        self.scoped_activity_results = self._update_activity_result_in_collection(
            self.scoped_activity_results, activity_name, status, output
        )

    def create_iteration_scope(self, iteration_item: Optional[str] = None) -> "PipelineRunState":
        """Used to create a new scope for a ControlActivity like ForEach, If and Until activities.

        Args:
            iteration_item: The current item() of a ForEach activity. If not supplied, takes parent iteration_item.

        Returns:
            A new PipelineRunState with the scoped variables and activity results.
        """
        return PipelineRunState(
            self.parameters,
            self.variables,
            self.activity_results,
            iteration_item if iteration_item is not None else self.iteration_item,
        )

    def add_scoped_activity_results_from_scoped_state(self, scoped_state: "PipelineRunState") -> None:
        """Registers all the activity results of a childScope into the current state.

        Args:
            scoped_state: The scoped childState.
        """
        for result in scoped_state.activity_results:
            self.activity_results = self._update_activity_result_in_collection(
                self.activity_results, result.activity_name, result.status, result.output
            )

    def try_get_activity_result_by_name(self, activity_name: str) -> Optional[Dict[str, Any]]:
        """Tries to get the activity result from the state. Might be None if the activity was not executed in the scope.

        Args:
            activity_name: Name of the activity.
        """
        return self._try_get_activity_result_from_collection_by_name(self.activity_results, activity_name)

    def get_activity_result_by_name(self, name: str) -> Dict[str, Any]:
        """Gets the activity result from the state. Throws an exception if the activity was not executed in the scope.

        Args:
            name: Name of the activity.
        """
        activity_result = self.try_get_activity_result_by_name(name)
        if activity_result is None:
            raise ActivityNotFoundError(name)

        return activity_result

    def set_variable(self, variable_name: str, value: DataFactoryObjectType) -> None:
        """Sets the value of a variable if it exists. Otherwise throws an exception.

        Args:
            variable_name: Name of the variable.
            value: New value of the variable.
        """
        for variable in self.variables:
            if variable.name == variable_name:
                variable.value = value
                return

        raise VariableBeingEvaluatedDoesNotExistError(variable_name)

    def append_variable(self, variable_name: str, value: DataFactoryObjectType) -> None:
        """Appends a value to a variable if it exists and is an array. Otherwise, throws an exception.

        Args:
            variable_name: Name of the variable.
            value: Appended value of the variable.
        """
        for variable in self.variables:
            if variable.name == variable_name:
                if not isinstance(variable.value, list):
                    raise ValueError(f"Variable {variable_name} is not an array.")

                variable.value.append(value)
                return

        raise VariableBeingEvaluatedDoesNotExistError(variable_name)

    def get_variable_by_name(self, variable_name: str) -> PipelineRunVariable:
        """Gets a variable by name. Throws an exception if the variable is not found.

        Args:
            variable_name: Name of the variable.
        """
        for variable in self.variables:
            if variable.name == variable_name:
                return variable

        raise VariableNotFoundError(variable_name)

    def set_return_value(self, param: str, evaluated_value: Any) -> None:  # noqa: ANN401
        self.return_values[param] = evaluated_value

    def get_parameter_by_type_and_name(self, parameter_type: RunParameterType, name: str) -> Any:  # noqa: ANN401
        """Gets the parameter by type and name. Throws an exception if the parameter is not found."""
        parameters = list(filter(lambda p: p.name == name and p.type == parameter_type, self.parameters))

        if len(parameters) == 0:
            raise ParameterNotFoundError(parameter_type, name)

        return parameters[0].value

    def is_activity_evaluated_in_scope(self, activity_name: str) -> bool:
        """Checks if an activity was evaluated in the current scope.

        Args:
            activity_name: Name of the activity.
        """
        return any(result.activity_name == activity_name for result in self.scoped_activity_results)

    @staticmethod
    def _try_get_activity_result_from_collection_by_name(
        activity_results: List[ActivityResult], name: str
    ) -> Optional[ActivityResult]:
        return next((result for result in activity_results if result.activity_name == name), None)

    @staticmethod
    def _update_activity_result_in_collection(
        activity_results: List[ActivityResult],
        activity_name: str,
        status: DependencyCondition,
        output: Any,  # noqa: ANN401
    ) -> List[ActivityResult]:
        activity_result = PipelineRunState._try_get_activity_result_from_collection_by_name(
            activity_results, activity_name
        )
        if activity_result:
            activity_result.status = status
            activity_result.output = output
        else:
            activity_results.append(ActivityResult(activity_name, status, output))

        return activity_results
