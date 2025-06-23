from typing import Any, Callable, Iterator, List, Optional

from data_factory_testing_framework.mock import ExpressionMock
from data_factory_testing_framework.models.activities._activity import Activity
from data_factory_testing_framework.state import PipelineRunState


class ControlActivity(Activity):
    """This is the base class for all control activities in the pipeline."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the base class for all control activities in the pipeline.

        Args:
            **kwargs: ControlActivity properties coming directly from the json representation of the activity.
        """
        super().__init__(**kwargs)

    def evaluate_control_activities(
        self,
        state: PipelineRunState,
        evaluate_activities: Callable[[List[Activity], PipelineRunState], Iterator[Activity]],
        mocks: Optional[List[ExpressionMock]] = None,
    ) -> Iterator[Activity]:
        yield from list()
