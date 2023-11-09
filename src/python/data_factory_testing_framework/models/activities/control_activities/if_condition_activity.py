from typing import Callable, Generator

from data_factory_testing_framework.generated.models import ForEachActivity, Activity, ControlActivity, \
    IfConditionActivity
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


class IfConditionActivity:

    def evaluate(self: IfConditionActivity, state: PipelineRunState):
        self.expression.evaluate(state)

        return super(ControlActivity, self).evaluate(state)

    def evaluate_control_activity_iterations(self: IfConditionActivity, state: PipelineRunState, evaluate_activities: Callable[[PipelineRunState], Generator[Activity, None, None]]):
        scoped_state = state.create_iteration_scope(None)
        activities = self.if_true_activities if self.expression.value else self.if_false_activities
        for activity in evaluate_activities(activities, scoped_state):
            yield activity

        state.add_scoped_activity_results_from_scoped_state(scoped_state)
