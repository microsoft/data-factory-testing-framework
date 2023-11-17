from typing import Any

from azure_data_factory_testing_framework.fabric.models.activities.fabric_control_activity import FabricControlActivity
from azure_data_factory_testing_framework.state import PipelineRunState


class FabricSetVariableActivity(FabricControlActivity):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Set Variable activity in the pipeline."""
        super(FabricControlActivity, self).__init__(*args, **kwargs)

    def evaluate(self, state: PipelineRunState) -> "FabricSetVariableActivity":
        super(FabricControlActivity, self).evaluate(state)

        if self.type_properties["variableName"] == "pipelineReturnValue":
            return self

        state.set_variable(self.type_properties["variableName"], self.type_properties["value"].evaluate(state))

        return self
