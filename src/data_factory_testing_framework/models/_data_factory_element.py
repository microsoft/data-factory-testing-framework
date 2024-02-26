import json
from typing import Any

from data_factory_testing_framework._functions.evaluator import ExpressionEvaluator
from data_factory_testing_framework.exceptions import (
    DataFactoryElementEvaluationError,
)
from data_factory_testing_framework.exceptions._user_error import UserError
from data_factory_testing_framework.models._data_factory_object_type import DataFactoryObjectType
from data_factory_testing_framework.state import RunState


class DataFactoryElement:
    expression: str
    result: DataFactoryObjectType

    def __init__(self, expression: str) -> None:
        """DataFactoryElement.

        Args:
            expression: Expression to evaluate. (e.g. @concat(@pipeline().parameters.pipelineName, '-pipeline'))
        """
        self.expression = expression
        self.result: DataFactoryObjectType = None

    def evaluate(self, state: RunState) -> DataFactoryObjectType:
        """Evaluate the expression."""
        try:
            evaluator = ExpressionEvaluator()
            self.result = evaluator.evaluate(self.expression, state)
        except UserError as e:
            raise e from e
        except Exception as e:
            raise DataFactoryElementEvaluationError(f"Error evaluating expression: {self.expression}") from e

        return self.result

    def get_json_value(self) -> Any:  # noqa: ANN401
        """Loads the value as a json object."""
        if self.result:
            return json.loads(self.result)

        return None
