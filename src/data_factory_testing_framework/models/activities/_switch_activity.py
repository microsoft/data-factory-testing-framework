from typing import Any, Callable, Dict, Generator, Iterator, List

from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities import Activity, ControlActivity
from data_factory_testing_framework.state import PipelineRunState


class SwitchActivity(ControlActivity):
    def __init__(
        self,
        default_activities: List[Activity],
        cases_activities: Dict[str, List[Activity]],
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """This is the class that represents the Switch activity in the pipeline.

        Args:
            default_activities: The deserialized activities that will be executed if none of the cases matches.
            cases_activities: The deserialized activities that will be executed if the case matches.
            **kwargs: SwitchActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "Switch"

        super(ControlActivity, self).__init__(**kwargs)

        self.default_activities = default_activities
        self.cases_activities = cases_activities
        self.on: DataFactoryElement = self.type_properties["on"]

    def evaluate(self, state: PipelineRunState) -> "SwitchActivity":
        evaluated_on = self.on.evaluate(state)
        if not isinstance(evaluated_on, str):
            raise ControlActivityExpressionEvaluatedNotToExpectedTypeError(self.name, str)

        super(ControlActivity, self).evaluate(state)

        return self

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
    ) -> Iterator[Activity]:
        for case, activities in self.cases_activities.items():
            if case == self.on.result:
                return self._run_activities_in_scope(state, activities, evaluate_activities)

        return self._run_activities_in_scope(state, self.default_activities, evaluate_activities)

    @staticmethod
    def _run_activities_in_scope(
        state: PipelineRunState,
        activities: List[Activity],
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
    ) -> Generator[Activity, None, None]:
        scoped_state = state.create_iteration_scope()
        for activity in evaluate_activities(activities, scoped_state):
            yield activity
        state.add_scoped_activity_results_from_scoped_state(scoped_state)
