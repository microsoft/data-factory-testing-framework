from typing import Callable, Generator

from azure_data_factory_testing_framework.generated.models import Activity, ControlActivity, UntilActivity
from azure_data_factory_testing_framework.state import PipelineRunState


class UntilActivity:
    def evaluate(self: UntilActivity, state: PipelineRunState) -> UntilActivity:
        self.expression.evaluate(state)

        return super(ControlActivity, self).evaluate(state)

    def evaluate_control_activity_iterations(
        self: UntilActivity,
        state: PipelineRunState,
        evaluate_activities: Callable[[PipelineRunState], Generator[Activity, None, None]],
    ) -> Generator[Activity, None, None]:
        while True:
            scoped_state = state.create_iteration_scope(None)
            for activity in evaluate_activities(self.activities, scoped_state):
                yield activity

            state.add_scoped_activity_results_from_scoped_state(scoped_state)

            if self.expression.evaluate(state):
                break
