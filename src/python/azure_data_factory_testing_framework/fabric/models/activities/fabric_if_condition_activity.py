from typing import Any, Callable, Generator

from azure_data_factory_testing_framework.fabric.models.activities.fabric_activity import FabricActivity
from azure_data_factory_testing_framework.fabric.models.activities.fabric_control_activity import FabricControlActivity
from azure_data_factory_testing_framework.state import PipelineRunState


class FabricIfConditionActivity(FabricControlActivity):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the If Condition activity in the pipeline."""
        super(FabricControlActivity, self).__init__(*args, **kwargs)

    def evaluate(self, state: PipelineRunState) -> "FabricIfConditionActivity":
        self.expression.evaluate(state)

        return super(FabricControlActivity, self).evaluate(state)

    def evaluate_control_activity_iterations(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[PipelineRunState], Generator[FabricActivity, None, None]],
    ) -> Generator[FabricActivity, None, None]:
        scoped_state = state.create_iteration_scope(None)
        activities = self.if_true_activities if self.expression.evaluated else self.if_false_activities
        for activity in evaluate_activities(activities, scoped_state):
            yield activity

        state.add_scoped_activity_results_from_scoped_state(scoped_state)
