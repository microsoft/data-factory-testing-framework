import json
from typing import Any, Generic, TypeVar, Union

from data_factory_testing_framework._functions.evaluator import ExpressionEvaluator
from data_factory_testing_framework.state import RunState

T = TypeVar("T")


class DataFactoryElement(Generic[T]):
    expression: str
    result: T

    def __init__(self, expression: str) -> None:
        """DataFactoryElement.

        Args:
            expression: Expression to evaluate. (e.g. @concat(@pipeline().parameters.pipelineName, '-pipeline'))
        """
        self.expression = expression
        self.result: Union[str, int, bool, float] = None

    def evaluate(self, state: RunState) -> Union[str, int, bool, float]:
        """Evaluate the expression."""
        evaluator = ExpressionEvaluator()
        self.result = evaluator.evaluate(self.expression, state)
        return self.result

    def get_json_value(self) -> Any:  # noqa: ANN401
        """Loads the value as a json object."""
        if self.result:
            return json.loads(self.result)

        return None
