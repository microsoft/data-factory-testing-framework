from typing import Any, Callable, Iterator, List

from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities import Activity, ControlActivity
from data_factory_testing_framework.state import DependencyCondition, PipelineRunState


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
        # Explicitly not evaluate here, but in the evaluate_control_activities method after the first iteration
        return self

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
    ) -> Iterator[Activity]:
        while True:
            scoped_state = state.create_iteration_scope()
            for activity in evaluate_activities(self.activities, scoped_state):
                yield activity

            state.add_scoped_activity_results_from_scoped_state(scoped_state)

            evaluated_expression = self.expression.evaluate(state)
            if not isinstance(evaluated_expression, bool):
                raise ControlActivityExpressionEvaluatedNotToExpectedTypeError(self.name, bool)

            if evaluated_expression:
                state.add_activity_result(self.name, DependencyCondition.Succeeded)
                self.set_result(DependencyCondition.Succeeded)
                break
