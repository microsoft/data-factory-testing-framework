from typing import Any

from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities import ControlActivity
from data_factory_testing_framework.state import DependencyCondition, PipelineRunState


class FilterActivity(ControlActivity):
    def __init__(
        self,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """This is the class that represents the If Condition activity in the pipeline.

        Args:
            **kwargs: FilterActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "Filter"

        super(ControlActivity, self).__init__(**kwargs)

        self.items: DataFactoryElement = self.type_properties["items"]
        self.condition: DataFactoryElement = self.type_properties["condition"]

    def evaluate(self, state: PipelineRunState) -> "FilterActivity":
        value = []
        for item in self.items.evaluate(state):
            state.iteration_item = item
            if self.condition.evaluate(state):
                value.append(item)

        self.set_result(DependencyCondition.SUCCEEDED, {"value": value})
        state.iteration_item = None

        return self
