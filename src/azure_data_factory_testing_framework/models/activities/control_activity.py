from typing import Any, Callable, Iterator, List

from azure_data_factory_testing_framework.models.activities.activity import Activity
from azure_data_factory_testing_framework.state import PipelineRunState


class ControlActivity(Activity):
    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the base class for all control activities in the pipeline.

        Args:
            **kwargs: ControlActivity properties coming directly from the json representation of the activity.
        """
        super(Activity, self).__init__(**kwargs)

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
    ) -> Iterator[Activity]:
        yield from list()
