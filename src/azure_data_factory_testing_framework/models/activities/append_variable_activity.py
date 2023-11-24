from typing import Any

from azure_data_factory_testing_framework.models.activities.control_activity import ControlActivity
from azure_data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.state import PipelineRunState


class AppendVariableActivity(ControlActivity):
    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Append Variable activity in the pipeline.

        Args:
            **kwargs: AppendVariableActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "AppendVariable"

        super(ControlActivity, self).__init__(**kwargs)

        self.variable_name: str = self.type_properties["variableName"]
        self.value: DataFactoryElement = self.type_properties["value"]

    def evaluate(self, state: PipelineRunState) -> "AppendVariableActivity":
        super(ControlActivity, self).evaluate(state)

        if isinstance(self.value, DataFactoryElement):
            evaluated_value = self.value.evaluate(state)
        else:
            evaluated_value = self.value

        state.append_variable(self.type_properties["variableName"], evaluated_value)

        return self
