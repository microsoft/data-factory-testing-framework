from typing import Any, List

from azure_data_factory_testing_framework.models.activities.activity_dependency import ActivityDependency
from azure_data_factory_testing_framework.models.activities.control_activity import ControlActivity
from azure_data_factory_testing_framework.state import PipelineRunState


class SetVariableActivity(ControlActivity):
    def __init__(self, name: str, depends_on: List[ActivityDependency] = None, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Set Variable activity in the pipeline."""
        if "type" not in kwargs:
            kwargs["type"] = "SetVariable"

        super(ControlActivity, self).__init__(name, depends_on, **kwargs)

    def evaluate(self, state: PipelineRunState) -> "SetVariableActivity":
        super(ControlActivity, self).evaluate(state)

        if self.type_properties["variableName"] == "pipelineReturnValue":
            return self

        state.set_variable(self.type_properties["variableName"], self.type_properties["value"].evaluate(state))

        return self
