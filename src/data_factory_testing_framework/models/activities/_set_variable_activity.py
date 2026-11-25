from typing import Any, List, Optional

from data_factory_testing_framework.mock import ExpressionMock
from data_factory_testing_framework.mock_context import MockContext
from data_factory_testing_framework.models._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.activities._control_activity import ControlActivity
from data_factory_testing_framework.state import PipelineRunState


class SetVariableActivity(ControlActivity):
    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """This is the class that represents the Set Variable activity in the pipeline.

        Args:
            **kwargs: SetVariableActivity properties coming directly from the json representation of the activity.
        """
        kwargs["type"] = "SetVariable"

        super().__init__(**kwargs)

        self.variable_name: str = self.type_properties["variableName"]
        self.value: DataFactoryElement = self.type_properties["value"]

    def evaluate(
        self,
        state: PipelineRunState,
        mocks: Optional[List[ExpressionMock]] = None
    ) -> "SetVariableActivity":
        mocks = mocks or []
        super().evaluate(state, mocks)
        

        if self.type_properties["variableName"] == "pipelineReturnValue":
            for return_value in self.type_properties["value"]:
                value = return_value["value"]
                if isinstance(value, DataFactoryElement):
                    evaluated_value = value.evaluate(
                        state,
                        mocks,
                        mock_context=MockContext(
                            pipeline=self.pipeline,
                            activity=self,
                            # TODO: Clarify what the property path should be here.
                            property_path=f"pipelineReturnValue.{return_value['key']}"
                        )
                    )
                else:
                    evaluated_value = value

                state.set_return_value(return_value["key"], evaluated_value)

            return self

        if isinstance(self.value, DataFactoryElement):
            evaluated_value = self.value.evaluate(
                state=state,
                mocks=mocks,
                mock_context=MockContext(
                    pipeline=self.pipeline,
                    activity=self,
                    property_path="value"
                )
            )
        else:
            evaluated_value = self.value

        state.set_variable(self.type_properties["variableName"], evaluated_value)

        return self
