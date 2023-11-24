from typing import Any, Callable, Iterator, List

from azure_data_factory_testing_framework.models.activities.activity import Activity
from azure_data_factory_testing_framework.models.activities.control_activity import ControlActivity
from azure_data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.state import PipelineRunState


class UntilActivity(ControlActivity):
    def __init__(
        self,
        activities: List[Activity],
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """This is the class that represents the Until activity in the pipeline.

        Args:
            activities: The deserialized activities that will be executed until the expression evaluates to true.
            **kwargs: UntilActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "Until"

        super(ControlActivity, self).__init__(**kwargs)

        self.expression: DataFactoryElement = self.type_properties["expression"]
        self.activities = activities

    def evaluate(self, state: PipelineRunState) -> "UntilActivity":
        self.expression.evaluate(state)

        super(ControlActivity, self).evaluate(state)

        return self

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
    ) -> Iterator[Activity]:
        while True:
            scoped_state = state.create_iteration_scope(None)
            for activity in evaluate_activities(self.activities, scoped_state):
                yield activity

            state.add_scoped_activity_results_from_scoped_state(scoped_state)

            if self.expression.evaluate(state):
                break
