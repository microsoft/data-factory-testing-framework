from typing import Callable, Generator

from azure_data_factory_testing_framework.generated.models import Activity, ControlActivity, ForEachActivity
from azure_data_factory_testing_framework.state import PipelineRunState


class ForEachActivity:
    def evaluate(self: ForEachActivity, state: PipelineRunState) -> ForEachActivity:
        self.items.evaluate(state)

        return super(ControlActivity, self).evaluate(state)

    def evaluate_control_activity_iterations(
        self: ForEachActivity,
        state: PipelineRunState,
        evaluate_activities: Callable[[PipelineRunState], Generator[Activity, None, None]],
    ) -> Generator[Activity, None, None]:
        for item in self.items.evaluated:
            scoped_state = state.create_iteration_scope(item)
            for activity in evaluate_activities(self.activities, scoped_state):
                yield activity

            state.add_scoped_activity_results_from_scoped_state(scoped_state)
