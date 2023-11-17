from typing import Any, Callable, Generator

from azure_data_factory_testing_framework.fabric.models.activities.fabric_activity import FabricActivity
from azure_data_factory_testing_framework.state import PipelineRunState


class FabricControlActivity(FabricActivity):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the base class for all control activities in the pipeline."""
        super(FabricActivity, self).__init__(*args, **kwargs)

    def evaluate_control_activity_iterations(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[PipelineRunState], Generator[FabricActivity, None, None]],
    ) -> Generator[FabricActivity, None, None]:
        yield from list()
