from typing import Any, List, Optional

from data_factory_testing_framework.mock import ExpressionMock
from data_factory_testing_framework.models.activities._control_activity import ControlActivity
from data_factory_testing_framework.state import DependencyCondition, PipelineRunState


class FailActivity(ControlActivity):
    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Fail activity in the pipeline.

        Args:
            **kwargs: FailActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "Fail"

        super(ControlActivity, self).__init__(**kwargs)

    def evaluate(
        self,
        state: PipelineRunState,
        mocks: Optional[List[ExpressionMock]] = None
    ) -> "FailActivity":
        mocks = mocks or []
        super().evaluate(state, mocks)

        self.set_result(DependencyCondition.FAILED)

        return self
