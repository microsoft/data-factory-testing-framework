from typing import Any

from azure_data_factory_testing_framework.models.activities.control_activity import ControlActivity
from azure_data_factory_testing_framework.state import PipelineRunState
from azure_data_factory_testing_framework.state.dependency_condition import DependencyCondition


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
