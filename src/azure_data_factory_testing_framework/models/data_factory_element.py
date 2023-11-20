from typing import Generic, TypeVar, Union

from azure_data_factory_testing_framework.functions import parse_expression
from azure_data_factory_testing_framework.state import RunState

T = TypeVar("T")


class DataFactoryElement(Generic[T]):
    expression: str
    value: T

    def __init__(self, expression: str) -> None:
        """DataFactoryElement.

        Args:
            expression: Expression to evaluate. (e.g. @concat(@pipeline().parameters.pipelineName, '-pipeline'))
        """
        self.expression = expression
        self.value: Union[str, int, bool, float] = None

    def evaluate(self, state: RunState) -> Union[str, int, bool, float]:
        self.value = parse_expression(self.expression).evaluate(state)
        return self.value
