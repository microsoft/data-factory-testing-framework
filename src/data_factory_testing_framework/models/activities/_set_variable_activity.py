from typing import Any

from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities import ControlActivity
from data_factory_testing_framework.state import PipelineRunState


class SetVariableActivity(ControlActivity):
    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Set Variable activity in the pipeline.

        Args:
            **kwargs: SetVariableActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "SetVariable"

        super(ControlActivity, self).__init__(**kwargs)

        self.variable_name: str = self.type_properties["variableName"]
        self.value: DataFactoryElement = self.type_properties["value"]

    def evaluate(self, state: PipelineRunState) -> "SetVariableActivity":
        super(ControlActivity, self).evaluate(state)

        if self.type_properties["variableName"] == "pipelineReturnValue":
            for return_value in self.type_properties["value"]:
                value = return_value["value"]
                if isinstance(value, DataFactoryElement):
                    evaluated_value = value.evaluate(state)
                else:
                    evaluated_value = value

                state.set_return_value(return_value["key"], evaluated_value)

            return self

        if isinstance(self.value, DataFactoryElement):
            evaluated_value = self.value.evaluate(state)
        else:
            evaluated_value = self.value

        state.set_variable(self.type_properties["variableName"], evaluated_value)

        return self
