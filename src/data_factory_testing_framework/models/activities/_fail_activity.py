from typing import Any

from data_factory_testing_framework.models.activities import ControlActivity
from data_factory_testing_framework.state import DependencyCondition, PipelineRunState


class FailActivity(ControlActivity):
    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Fail activity in the pipeline.

        Args:
            **kwargs: FailActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "Fail"

        super(ControlActivity, self).__init__(**kwargs)

    def evaluate(self, state: PipelineRunState) -> "FailActivity":
        super(ControlActivity, self).evaluate(state)

        self.set_result(DependencyCondition.FAILED)

        return self
