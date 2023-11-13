from typing import Callable, Generator

from data_factory_testing_framework.generated.models import Activity
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


class ControlActivity:
    def evaluate_control_activity_iterations(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[PipelineRunState], Generator[Activity, None, None]],
    ):
        return []
