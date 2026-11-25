from typing import Any, Callable, Dict, Generator, Iterator, List, Optional

from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.mock import ExpressionMock
from data_factory_testing_framework.mock_context import MockContext
from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities._activity import Activity
from data_factory_testing_framework.models.activities._control_activity import ControlActivity
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


    @property
    def nested_activities(self) -> List["Activity"]:
        """Get the nested activities of this activity."""
        return self.default_activities + [activity for activities in self.cases_activities.values() for activity in activities]

    def evaluate(
            self,
            state: PipelineRunState,
            mocks: Optional[List[ExpressionMock]] = None,
        ) -> "SwitchActivity":
        mocks = mocks or []
        evaluated_on = self.on.evaluate(state, mocks, mock_context=MockContext(
            pipeline=self.pipeline,
            activity=self,
            property_path="on"
        ))
        if not isinstance(evaluated_on, str):
            raise ControlActivityExpressionEvaluatedNotToExpectedTypeError(self.name, str)

        super().evaluate(state, mocks)

        return self

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
        mocks: List[ExpressionMock],
    ) -> Iterator[Activity]:
        for case, activities in self.cases_activities.items():
            if case == self.on.result:
                return self._run_activities_in_scope(state, activities, evaluate_activities, mocks)

        return self._run_activities_in_scope(state, self.default_activities, evaluate_activities, mocks)

    @staticmethod
    def _run_activities_in_scope(
        state: PipelineRunState,
        activities: List[Activity],
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
        mocks: Optional[List[ExpressionMock]] = None,
    ) -> Generator[Activity, None, None]:
        mocks = mocks or []
        scoped_state = state.create_iteration_scope()
        for activity in evaluate_activities(activities, scoped_state, mocks):
            yield activity
        state.add_scoped_activity_results_from_scoped_state(scoped_state)
