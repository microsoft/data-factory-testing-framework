from typing import Callable, Generator

from azure_data_factory_testing_framework.generated.models import (
    Activity,
    ControlActivity,
    IfConditionActivity,
)
from azure_data_factory_testing_framework.state import PipelineRunState


class IfConditionActivity:
    def evaluate(self: IfConditionActivity, state: PipelineRunState) -> IfConditionActivity:
        self.expression.evaluate(state)

        return super(ControlActivity, self).evaluate(state)

    def evaluate_control_activity_iterations(
        self: IfConditionActivity,
        state: PipelineRunState,
        evaluate_activities: Callable[[PipelineRunState], Generator[Activity, None, None]],
    ) -> Generator[Activity, None, None]:
        scoped_state = state.create_iteration_scope(None)
        activities = self.if_true_activities if self.expression.evaluated else self.if_false_activities
        for activity in evaluate_activities(activities, scoped_state):
            yield activity

        state.add_scoped_activity_results_from_scoped_state(scoped_state)
