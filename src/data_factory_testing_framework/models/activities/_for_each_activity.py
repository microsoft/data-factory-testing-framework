from typing import Any, Callable, Iterator, List, Optional

from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.mock import ExpressionMock
from data_factory_testing_framework.mock_context import MockContext
from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities._activity import Activity
from data_factory_testing_framework.models.activities._control_activity import ControlActivity
from data_factory_testing_framework.state import PipelineRunState


class ForEachActivity(ControlActivity):
    def __init__(
        self,
        activities: List[Activity],
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """This is the class that represents the For Each activity in the pipeline.

        Args:
            activities: The deserialized activities that will be executed for each item in the items array.
            **kwargs: ForEachActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "ForEach"

        super().__init__(**kwargs)

        self.activities = activities
        self.items: DataFactoryElement = self.type_properties["items"]

    @property
    def nested_activities(self) -> List["Activity"]:
        """Get the nested activities of this activity."""
        return self.activities

    def evaluate(
            self,
            state: PipelineRunState,
            mocks: Optional[List[ExpressionMock]] = None
    ) -> "ForEachActivity":
        mocks = mocks or []
        items = self.items.evaluate(state, mocks=mocks, mock_context=MockContext(pipeline=self.pipeline, activity=self, property_path="items"))

        if not isinstance(items, list):
            raise ControlActivityExpressionEvaluatedNotToExpectedTypeError(self.name, list)

        super().evaluate(state, mocks)

        return self

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
        mocks: Optional[List[ExpressionMock]] = None
    ) -> Iterator[Activity]:
        mocks = mocks or []
        for item in self.items.result:
            scoped_state = state.create_iteration_scope(item)
            for activity in evaluate_activities(self.activities, scoped_state, mocks):
                yield activity

            state.add_scoped_activity_results_from_scoped_state(scoped_state)
