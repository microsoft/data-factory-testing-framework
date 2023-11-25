from typing import Generic, TypeVar, Union

from azure_data_factory_testing_framework.functions.expression_evaluator import ExpressionEvaluator
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
        """Evaluate the expression."""
        evaluator = ExpressionEvaluator()
        self.value = evaluator.evaluate(self.expression, state)
        return self.value
