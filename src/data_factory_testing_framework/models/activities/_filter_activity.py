from typing import Any, List, Optional

from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.mock import ExpressionMock
from data_factory_testing_framework.mock_context import MockContext
from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities._control_activity import ControlActivity
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

        super().__init__(**kwargs)

        self.items: DataFactoryElement = self.type_properties["items"]
        self.condition: DataFactoryElement = self.type_properties["condition"]

    def evaluate(
        self,
        state: PipelineRunState,
        mocks: Optional[List[ExpressionMock]] = None
    ) -> "FilterActivity":
        mocks = mocks or []
        mock_context = MockContext(
            pipeline=self.pipeline,
            activity=self,
            property_path="items"
        )
        items = self.items.evaluate(state, mocks=mocks, mock_context=mock_context)
        if not isinstance(items, list):
            raise ControlActivityExpressionEvaluatedNotToExpectedTypeError(self.name, list)

        value = []
        for item in items:
            scoped_state = state.create_iteration_scope(item)
            if self.condition.evaluate(
                scoped_state,
                mocks,
                mock_context=MockContext(
                    pipeline=self.pipeline,
                    activity=self,
                    property_path="condition",
                )
            ):
                value.append(item)

        self.set_result(DependencyCondition.SUCCEEDED, {"value": value})

        return self
