from typing import Any

from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities import ControlActivity
from data_factory_testing_framework.state import DependencyCondition, PipelineRunState


class FilterActivity(ControlActivity):
    def __init__(
        self,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """This is the class that represents the Filter activity in the pipeline.

        Args:
            **kwargs: FilterActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "Filter"

        super(ControlActivity, self).__init__(**kwargs)

        self.items: DataFactoryElement = self.type_properties["items"]
        self.condition: DataFactoryElement = self.type_properties["condition"]

    def evaluate(self, state: PipelineRunState) -> "FilterActivity":
        items = self.items.evaluate(state)
        if not isinstance(items, list):
            raise ControlActivityExpressionEvaluatedNotToExpectedTypeError(self.name, list)

        value = []
        for item in items:
            scoped_state = state.create_iteration_scope(item)
            if self.condition.evaluate(scoped_state):
                value.append(item)

        self.set_result(DependencyCondition.SUCCEEDED, {"value": value})

        return self
