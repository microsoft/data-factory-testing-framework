from typing import Any, Callable, Iterator, List

from data_factory_testing_framework.models.activities.activity import Activity
from data_factory_testing_framework.models.activities.control_activity import ControlActivity
from data_factory_testing_framework.models.data_factory_element import DataFactoryElement
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

        super(ControlActivity, self).__init__(**kwargs)

        self.activities = activities
        self.items: DataFactoryElement = self.type_properties["items"]

    def evaluate(self, state: PipelineRunState) -> "ForEachActivity":
        self.items.evaluate(state)

        super(ControlActivity, self).evaluate(state)

        return self

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
    ) -> Iterator[Activity]:
        for item in self.items.result:
            scoped_state = state.create_iteration_scope(item)
            for activity in evaluate_activities(self.activities, scoped_state):
                yield activity

            state.add_scoped_activity_results_from_scoped_state(scoped_state)
