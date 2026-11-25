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


class IfConditionActivity(ControlActivity):
    def __init__(
        self,
        if_true_activities: List[Activity],
        if_false_activities: List[Activity],
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """This is the class that represents the If Condition activity in the pipeline.

        Args:
            if_true_activities: The deserialized activities that will be executed if the condition is true.
            if_false_activities: The deserialized activities that will be executed if the condition is false.
            **kwargs: IfConditionActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "IfCondition"

        super(ControlActivity, self).__init__(**kwargs)

        self.if_true_activities = if_true_activities
        self.if_false_activities = if_false_activities
        self.expression: DataFactoryElement = self.type_properties["expression"]

    @property
    def nested_activities(self) -> List["Activity"]:
        """Get the nested activities of this activity."""
        return self.if_true_activities + self.if_false_activities

    def evaluate(
            self,
            state: PipelineRunState,
            mocks: Optional[List[ExpressionMock]] = None,
        ) -> "IfConditionActivity":
        mocks = mocks or []
        evaluated_expression = self.expression.evaluate(state, mocks, MockContext(
            pipeline=self.pipeline,
            activity=self,
            property_path="expression"
        ))
        if not isinstance(evaluated_expression, bool):
            raise ControlActivityExpressionEvaluatedNotToExpectedTypeError(self.name, bool)

        super().evaluate(state, mocks)

        return self

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
        mocks: Optional[List[ExpressionMock]] = None,
    ) -> Iterator[Activity]:
        scoped_state = state.create_iteration_scope()
        activities = self.if_true_activities if self.expression.result else self.if_false_activities
        for activity in evaluate_activities(activities, scoped_state, mocks):
            yield activity

        state.add_scoped_activity_results_from_scoped_state(scoped_state)
