from typing import Any, Callable, Generator, List

from azure_data_factory_testing_framework.models.activities.activity import Activity
from azure_data_factory_testing_framework.models.activities.control_activity import ControlActivity
from azure_data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.state import PipelineRunState


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

    def evaluate(self, state: PipelineRunState) -> "IfConditionActivity":
        self.expression.evaluate(state)

        super(ControlActivity, self).evaluate(state)

        return self

    def evaluate_control_activity_iterations(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[PipelineRunState], Generator[Activity, None, None]],
    ) -> Generator[Activity, None, None]:
        scoped_state = state.create_iteration_scope(None)
        activities = self.if_true_activities if self.expression.value else self.if_false_activities
        for activity in evaluate_activities(activities, scoped_state):
            yield activity

        state.add_scoped_activity_results_from_scoped_state(scoped_state)
